from django.contrib import admin
from django.urls import path
from website.urls import urlpatterns as principal_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls)
] + principal_urls


# add this lines
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)