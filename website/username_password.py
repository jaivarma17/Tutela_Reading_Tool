from django.contrib.auth.models import User

# Create users with specific usernames and passwords
User.objects.create_user(username='user1', password='password1')
User.objects.create_user(username='user2', password='password2')



# Create a user with username and password
User.objects.create_user(username='custom_user', password='custom_password')
