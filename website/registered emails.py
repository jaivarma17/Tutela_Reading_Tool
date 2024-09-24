from .models import RegisteredEmail

def register_user(email, password):
    # Code to register user
    if not RegisteredEmail.objects.filter(email=email).exists():
        RegisteredEmail.objects.create(email=email)

# Retrieve all registered emails
def get_all_registered_emails():
    return RegisteredEmail.objects.values_list('email', flat=True)

