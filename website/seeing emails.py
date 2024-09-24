from website.models import RegisteredEmail
emails = RegisteredEmail.objects.all()
for email in emails:
    print(email.email)