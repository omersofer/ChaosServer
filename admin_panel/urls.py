from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^normal', views.normal, name='normal'),
    url(r'^degraded', views.degraded, name='degraded'),
    url(r'^failure', views.failure, name='failure'),
]
