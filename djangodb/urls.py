"""
URL configuration for djangodb project.

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
'''from django.contrib import admin
from django.urls import path, include
from .views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),

    path('login/', login_view, name='login'),
    path('success/', success_view, name='success'),  
]'''

from django.contrib import admin
from django.urls import path, include
from website import views



urlpatterns = [
    #path('/', views.home, name='home.html'),
    #path('student/login/', views.submit_login, name='submit_login'),
    path('admin/', admin.site.urls),
    path(' ', include('website.urls')),  # Namespace for app URLs
    #path('student/login/', views.submit_login, name='submit_login'),
    path('register/', views.register_view, name='registration'),
    path('student/index/', views.index, name='index.html'),
    path('homepage/', views.homepage, name='homepage.html'),
    path('student/index/homepage.html', views.homepage, name='homepage_html'),
    #path('submit-form/', views.submit_form, name='submit_form'),  
    path('student/index/submit.html', views.submit, name='submit.html'),
    path('student/index/thankyou.html', views.thankyou, name='thankyou.html'),
    path('emails/', views.email_list_view, name='email_list.html'),
    path('log/', views.submit_login, name='login'),
    #path('homescreen.html/', views.homepage, name='homescreen.html'),
    path('log/ad-home/', views.homescreen, name='homescreen'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/add/', views.add_article, name='add_article'),
    #path('articles/delete/<int:pk>/', views.confirm_delete, name='confirm_delete'),
    #path('articles/delete/<int:pk>/', views.delete_article, name='delete_article'),
    #path('articles/confirm_delete/<int:pk>/', views.confirm_delete, name='confirm_delete'),
    path('articles/delete/<int:pk>/', views.delete_article, name='delete_article'),
    path('users/', views.users, name='users'),
    path('ai-key/', views.ai_key_view, name='ai_key'),
    path('fetch-articles/', views.fetch_articles, name='fetch_articles'),
    path('options/', views.options_view, name='options'),
    path('resume-registration/', views.resume_registration_view, name='resume_registration'),
    #path('pause-registration/', views.user_pause_registration, name='pauseregistration'),
    path('pause-registration/', views.pause_registration_view, name='pause_registration'),
    path('pause-registration/<str:username>/', views.pause_registration_view, name='pause_registration'),
    path('resume-registration/<str:username>/', views.resume_registration_view, name='resume_registration'),
    path('pause_resume/<str:username>/', views.pause_resume_user, name='pause_resume_user'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('send-notification/', views.send_notification_emails, name='send_notification')
    
]
    




