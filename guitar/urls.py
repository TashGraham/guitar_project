from django.urls import path
from guitar import views

app_name = 'guitar'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]