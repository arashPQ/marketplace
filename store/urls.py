from django.urls import path
from . import views

app_name = "store"


urlpatterns = [
    path('', views.index ,name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('user_configur/', views.user_configuration, name='user_configuration'),
    path('inf_configur/', views.info_configuration, name="info_configuration"),
    path('pass_configur/', views.pass_configuration, name='pass_configuration'),
    path('pruduct/<int:pk>', views.product, name='product'),
    path('Category/<str:cn>', views.category, name='category'),
    path('Category/<str:sn>', views.subcategory, name='subcategory'),
    path('search/', views.search, name='search'),



]
