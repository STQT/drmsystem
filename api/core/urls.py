from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("v1/", include("core.api_router"), name="v1"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = "Dashboard Svitlogorie"
admin.site.site_header = "Dashboard Svitlogorie"
admin.site.site_url = "https://t.me/" + settings.BOT_USERNAME
admin.site.index_title = "Svitlogorie.ru"
