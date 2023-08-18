import json
import logging
import os
import requests

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import F, ExpressionWrapper, DurationField

from celery import shared_task
from .models import Order, Subscriber

User = get_user_model()


@shared_task
def getting_order_photo(order_id):
    instance = Order.objects.get(pk=order_id)
    file_id = instance.photo_uri
    file_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile"
    params = {"file_id": file_id}
    response = requests.get(file_url, params=params)
    file_data = response.json()

    # Get the file_path from the Telegram API response
    file_path = file_data['result']['file_path']

    # Download the photo from Telegram and save it to your desired location
    photo_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
    photo_response = requests.get(photo_url)

    directory = os.path.join(settings.MEDIA_ROOT, 'cache')
    os.makedirs(directory, exist_ok=True)
    photo_filename = file_path.split('/')[-1]

    photo_path = os.path.join(directory, photo_filename)
    with open(photo_path, 'wb') as f:
        f.write(photo_response.content)

    instance.photo = os.path.join('cache', photo_filename)
    instance.save()
    return f"Photo for Order {order_id} downloaded and saved successfully."


@shared_task
def create_subscription(order_id, user_id, days):
    subscription = Subscriber.objects.filter(user_id=user_id,
                                             user__is_subscribed=True).select_related("user")
    if subscription.exists():
        subscription = subscription.first()
        subscription.created_at = timezone.now()
        subscription.order_id = order_id
        subscription.days = F('days') + days
        subscription.save()
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": user_id,
            "text": f"Ваш запрос на продление подписки одобрили."
        }
        response = requests.post(url, data=data)
        # Check if the request was successful
        if response.status_code == 200:
            logging.info("Message sent successfully.")
        else:
            logging.warning(f"Failed to send message. Status code: {response.status_code}")
            logging.warning(response.text)
    else:
        creation_link_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/createChatInviteLink"
        expire_date = int(timezone.now().timestamp()) + 86400
        params = {
            "chat_id": str(settings.TELEGRAM_BOT_CONTENT_CHAT_ID),
            "name": str(order_id),
            "expire_date": expire_date,
            "member_limit": 1,
        }
        link_resp = requests.get(url=creation_link_url, params=params)
        if link_resp.status_code == 200:
            logging.info("Link create successfully.")
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": user_id,
                "text": f"Сіздің жазылым сілтемеңіз {link_resp.json()['result']['invite_link']}. 1 күнге жарамды."
            }
            response = requests.post(url, data=data)

            # Check if the request was successful
            if response.status_code == 200:
                logging.info("Message sent successfully.")
            else:
                logging.warning(f"Failed to send message. Status code: {response.status_code}")
                logging.warning(response.text)
            Subscriber.objects.create(order_id=order_id, user_id=user_id, days=days)
            user = User.objects.get(id=user_id)
            user.is_subscribed = True
            user.save()
        else:
            logging.warning(f"Failed to send message. Status code: {link_resp.status_code}")
            logging.warning(link_resp.text)


@shared_task
def periodically_kick_expired_users():
    expired_subscribers = Subscriber.objects.annotate(
        expiration_time=F('created_at') + ExpressionWrapper(F('days') * timezone.timedelta(days=1),
                                                            output_field=DurationField())
    ).filter(expiration_time__lte=timezone.now()).select_related("user")
    until_date = int(timezone.now().timestamp()) + 40
    for subscriber in expired_subscribers:
        try:
            requests.get(
                f'https://api.telegram.org/bot{str(settings.TELEGRAM_BOT_TOKEN)}'
                f'/banChatMember?chat_id={str(settings.TELEGRAM_BOT_CONTENT_CHAT_ID)}'
                f'&user_id={str(subscriber.user.id)}'
                f'&until_date={str(until_date)}')
            subscriber.delete()
        finally:
            logging.info(f"Successfully deleted expired subscription user: {subscriber.user.id}")


@shared_task
def sending_notify_for_expiration_users():
    expired_subscribers = Subscriber.objects.annotate(
        expiration_time=F('created_at') + ExpressionWrapper(F('days') * timezone.timedelta(days=1),
                                                            output_field=DurationField())
    ).filter(expiration_time__lte=timezone.now() + timezone.timedelta(days=1)).select_related("user")
    text = ("Сіздің жазылымыңыздың бітуіне 1 күн қалды, жазылымды ұзартып үлгеріңіз"
            "сонда сізге қосымша 1 күн жазылым қосып береміз")
    inline_keyboard = {
        "inline_keyboard": [
            [{"text": "📅 Жазылымды жаңарту", "callback_data": "upgrade"}, ]
        ]
    }
    keyboard_json = json.dumps(inline_keyboard)
    for subscriber in expired_subscribers:
        try:
            data = {
                "chat_id": str(subscriber.user.id),
                "text": text,
                'reply_markup': keyboard_json
            }
            requests.post(
                f'https://api.telegram.org/bot{str(settings.TELEGRAM_BOT_TOKEN)}/sendMessage',
                data=data)
        finally:
            logging.info(f"Sending expiration notification to user: {subscriber.user.id}")
