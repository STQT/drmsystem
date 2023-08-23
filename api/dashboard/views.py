# dashboard_app/views.py
from main.models import Organization
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
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
    organizations = Organization.objects.all()

    return render(request, 'dashboard/dashboard.html', {
        'total_users': total_users,
        'active_users': active_users,
        'active_orders': active_orders,
        'total_subscribers': total_subscribers,
        'organizations': organizations,
    })


@cache_page(60 * 15)
def get_orders_data(request):
    orders_data = Order.objects.annotate(
        created_day=TruncDay('created_at')
    ).values('created_day').annotate(count=Count('id'))

    formatted_data = []
    for entry in orders_data:
        date = entry['created_day']
        formatted_date = timezone.localtime(date).strftime('%Y-%m-%d')
        formatted_data.append({'created_day': formatted_date, 'count': entry['count']})

    return JsonResponse({'data': formatted_data})


@cache_page(60 * 15)
def get_subscribers_data(request):
    subscribers_data = Subscriber.objects.annotate(
        created_day=TruncDay('created_at')
    ).values('created_day').annotate(count=Count('id'))

    formatted_data = []
    for entry in subscribers_data:
        date = entry['created_day']
        formatted_date = timezone.localtime(date).strftime('%Y-%m-%d')
        formatted_data.append({'created_day': formatted_date, 'count': entry['count']})

    return JsonResponse({'data': formatted_data})


@login_required
def get_detail_organization(request, slug):
    organization = get_object_or_404(Organization, slug=slug)

    context = {
        'obj': organization,
    }

    return render(request, 'dashboard/organization.html', context)
