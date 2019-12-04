from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url

from .views import about_page, contact_page, signup, HomeTemplateView, update_profile

urlpatterns = [
    path('finances/', include('finances.urls')),
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', signup, name='signup'),

    path('', HomeTemplateView.as_view(), name='home'),
    re_path(r'^about/$', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('update_profile/<int:pk>/', update_profile, name='update_profile'),


]
