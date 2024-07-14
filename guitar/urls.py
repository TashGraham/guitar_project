from django.urls import path
from guitar import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'guitar'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('<slug:category_name_slug>/<slug:part_name_slug>/', views.show_part, name='show_part'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)