from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from .models import Article
import os

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    mothers_email = forms.EmailField(label="Mother's Email", required=True)
    fathers_email = forms.EmailField(label="Father's Email", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'mothers_email', 'fathers_email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            
            mothers_email = self.cleaned_data.get('mothers_email') or "None"
            fathers_email = self.cleaned_data.get('fathers_email') or "None"
            
            # Correct format for userdetails.txt
            file_path = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Append the new user information to userdetails.txt
            with open(file_path, 'a') as file:
                file.write(f"Username: {user.username}, Email: {user.email}, Mother's Email: {mothers_email}, Father's Email: {fathers_email}, Status: active\n")
        return user



class YourForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class LoginForms(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['ArticleWebsite', 'ArticleNumber', 'ArticleName', 'ArticleURL']

class YF(forms.Form):
    article = forms.CharField(widget=forms.Textarea, required=True, label="Article")
    userInput = forms.CharField(widget=forms.Textarea, required=True, label="Summary")