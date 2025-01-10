"""
URL configuration for temp_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('create-post/', views.create_post, name='create_post'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),  
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),  
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('subscription/', views.subscription_page, name='subscription_page'),
    path('payment/<int:amount>/', views.payment_page, name='payment_page'),
    path('payment-success/', views.payment_success, name='payment_success'),

]
