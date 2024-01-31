from django.urls import path,re_path
from . import views

app_name = 'user'

urlpatterns = [
    re_path(r'^login/$', views.signin, name='login'),
    re_path(r'^registration/$', views.sign_up, name='signup'),
]