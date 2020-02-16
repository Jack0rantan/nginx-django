from django.urls import path

from . import views

app_name ="develop" 

urlpatterns = [
    path('', views.index, name='index'),
    path('develop/coin', views.coin, name='coin'),
    
]