from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url

from .views import home_page, about_page, contact_page, example_page, signup

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home_page, name='home'),
    re_path(r'^about/$', about_page),
    path('contact', contact_page),
    path('example', example_page),
    path('admin/', admin.site.urls),
]
