from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', show_home2, name='index'),
    path('list_subjects', show_list_subjects, name='list_subjects'),
    path('list_executor/<int:pk>', show_list_executor, name='list_executor'),
    path('executor/<int:pk>', show_executor, name='executor'),
    path('login', show_login, name='login'),
    path('register', show_register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)