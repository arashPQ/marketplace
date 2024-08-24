from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ,name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('user_configur/', views.user_configuration, name='user_configuration'),
    path('password_configur/', views.password_configuration, name='password_configuration'),
    path('pruduct/<int:pk>', views.product, name='product'),
    path('Category/<str:cn>', views.category, name='category'),

]
