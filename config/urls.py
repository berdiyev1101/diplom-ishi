from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from config import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("shop.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document=settings.MEDIA_ROOT)

