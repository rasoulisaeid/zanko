
import imp
from django import views
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static, serve
from .router import router
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),                  
    path('api/', include(router.urls)),
    path('api/', include('auth.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
