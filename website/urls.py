'''from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from .views import login_view, success_view


urlpatterns = [

    path('login/', login_view, name='login'),  # Ensure this is correctly defined
    path('success/', success_view, name='success'),
    path('', views.home, name='home'),  # This is valid
    path('submit-login/', views.submit_login, name='submit_login'),  # This is valid
    path('admin/', admin.site.urls),
    path('', include('website.urls')),

]'''

from django.urls import path
from .views import login_view, success_view, register_view, email_list_view, homescreen, add_article, delete_article, ai_key_view, options_view, register_view, pause_registration_view, resume_registration_view, remove_user_view, send_notification_emails


urlpatterns = [
    path('login/', login_view, name='login'),
    path('success/', success_view, name='success'),
    path('register/', register_view, name='registration'),
    path('emails/', email_list_view, name='email_list'),
    path('home/', homescreen, name='homescreen.html'),
    path('articles/delete/<int:pk>/', delete_article, name='delete_article'),
    path('ai-key/', ai_key_view, name='ai_key'),\
    path('options/', options_view, name='options'),
    path('register/', register_view, name='register_view'),
    path('remove-user/<str:username>/', remove_user_view, name='remove_user'),
    path('send-notification/', send_notification_emails, name='send_notification'),
]
