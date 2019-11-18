from django.contrib import admin
from django.urls import path, re_path

from .views import home_page, about_page, contact_page, example_page

urlpatterns = [
    path('', home_page),
    re_path(r'^about/$', about_page),
    path('contact', contact_page),
    path('example', example_page),
    path('admin/', admin.site.urls),
]
