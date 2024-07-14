from django.urls import path
from guitar import views
from django.contrib.auth.views import LogoutView

app_name = 'guitar'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/',
         views.show_category, name='show_category'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
]