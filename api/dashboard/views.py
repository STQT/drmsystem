# dashboard_app/views.py
from django.shortcuts import render
from orders.models import Order, Subscriber
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.views.decorators.cache import cache_page

User = get_user_model()


@login_required
@cache_page(60 * 15)
def dashboard(request):
    total_users = User.objects.count()
    active_users = User.objects.filter(stopped=False).count()
    active_orders = Order.objects.count()
    total_subscribers = Subscriber.objects.count()

    return render(request, 'dashboard/dashboard.html', {
        'total_users': total_users,
        'active_users': active_users,
        'active_orders': active_orders,
        'total_subscribers': total_subscribers,
    })


@cache_page(60 * 15)
def get_orders_data(request):
    orders_data = Order.objects.annotate(created_day=TruncDay('created_at')).values(
        'created_day').annotate(count=Count('id'))
    return JsonResponse({'data': list(orders_data)})


@cache_page(60 * 15)
def get_subscribers_data(request):
    subscribers_data = Subscriber.objects.annotate(
        created_day=TruncDay('created_at')
    ).values('created_day').annotate(count=Count('id'))
    return JsonResponse({'data': list(subscribers_data)})
