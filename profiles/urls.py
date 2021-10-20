from django.urls import path
from . import views

urlpatterns = [
    path('', views.update_profile_page, name='update_profile_page'),
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('delete/', views.delete_user_page, name='delete_user_page'),
]
