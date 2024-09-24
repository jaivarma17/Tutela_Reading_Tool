import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Member
from .models import Article
from django.http import HttpResponse
from .forms import YourForm
from .models import SubmissionCount
from django.utils import timezone
from datetime import timedelta
from .forms import LoginForms
from .forms import RegistrationForm
from .models import RegisteredEmail
from .forms import ArticleForm 
from django.conf import settings
from django.urls import reverse
from .utils import gpt_check_summary
import openai
from openai import OpenAIError
from django.http import JsonResponse
from .models import Article
from django.views.decorators.csrf import csrf_protect
from .utils import pause_registration, resume_registration
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.hashers import make_password, check_password
openai.api_key = settings.OPENAI_API_KEY

ALLOWED_USERS = {
    'Jai': make_password('1234'),
    # Add more users as needed
}

def submit_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username is in the custom dictionary
        if username in ALLOWED_USERS and check_password(password, ALLOWED_USERS[username]):
            # Authenticate the user using Django's authentication system
            user = authenticate(request, username=username, password=password)
            login(request)

                # Redirect to a success page or home page
            return redirect('homescreen')  # Replace 'homescreen' with the name of your URL pattern for the home page
            # else:
            #     return HttpResponse('Invalid credentials', status=401)
        else:
            return HttpResponse('Username not allowed or incorrect password', status=403)
    else:
        # Render a login form or page
        return render(request, 'login.html')

def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')  # Redirect to the article list after deletion
    return render(request, 'confirm_delete.html', {'article': article})


def homescreen(request):
    return render(request, 'homescreen.html') 



def homepage(request):
    # Retrieve the list of displayed article IDs from the session
    displayed_article_ids = request.session.get('displayed_article_ids', [])
    
    # Get all articles that have not been displayed yet
    available_articles = Article.objects.exclude(id__in=displayed_article_ids)
    
    # Check if there are any available articles left to display
    if available_articles.count() > 0:
        # Select 2 random articles from the available ones
        articles = list(available_articles)
        if len(articles) > 2:
            articles = random.sample(articles, 2)
        else:
            articles = articles
        
        # Update the session with new displayed articles
        new_displayed_article_ids = [article.id for article in articles]
        displayed_article_ids.extend(new_displayed_article_ids)
        request.session['displayed_article_ids'] = displayed_article_ids
        
    else:
        # All articles have been displayed, reset the session
        request.session['displayed_article_ids'] = []
        articles = []  # No articles to display
    
    return render(request, 'homepage.html', {'articles': articles})

def fetch_articles(request):
    articles = Article.objects.values('ArticleWebsite', 'ArticleName', 'ArticleNumber')  # Only get specific fields
    return JsonResponse({'articles': list(articles)})
    
def success(request):
    return HttpResponse('Login successful!')

def success_view(request):
    return render(request, 'success.html') 

def login(request):
	return render(request, 'login.html', {'all':all_articles})

def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request)
            return redirect('login.html')  # Redirect to a success page or dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def login(request):
    return render(request, 'login.html')

def article_list(request):
    articles = Article.objects.all()  
    return render(request, 'article_list.html', {'articles': articles})


# def parse_user_line(line):
#     # Remove leading and trailing whitespace
#     line = line.strip()

#     # Check for line format
#     if not line or not line.startswith('Username:'):
#         raise ValueError(f"Line format is incorrect: {line}")

#     # Split the line into parts based on commas
#     parts = line.split(', ')
#     if len(parts) < 3:
#         raise ValueError(f"Line format is incorrect: {line}")

#     # Extract each part
#     try:
#         name = parts[0].split(': ')[1]
#         email = parts[1].split(': ')[1]
#         parents_email = parts[2].split(': ')[1]
#         # Handle optional status field if present
#         status = parts[3].split(': ')[1] if len(parts) > 3 else 'active'  # Default to 'active'
#     except IndexError as e:
#         raise ValueError(f"Line format is incorrect: {line}. Error: {e}")

#     return {
#         'name': name,
#         'email': email,
#         'parents_email': parents_email,
#         'status': status
#     }

def parse_user_line(line):
    parts = line.strip().split(', ')
    if len(parts) == 5:  # Now expect 5 parts
        return {
            'name': parts[0].split(': ')[1],
            'email': parts[1].split(': ')[1],
            'mothers_email': parts[2].split(': ')[1],  # Update key for mother's email
            'fathers_email': parts[3].split(': ')[1],  # Update key for father's email
            'status': parts[4].split(': ')[1]  # Extract status
        }
    raise ValueError(f"Line format is incorrect: {line}")


# def users(request):
#     # Define the file path
#     file_path = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')

#     # Read and parse the data from the file
#     users_data = []
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#             for line in lines:
#                 if line.strip():  # Skip empty lines
#                     user_data = parse_user_line(line)
#                     users_data.append(user_data)

#     # Pass the parsed data to the template
#     return render(request, 'users.html', {'users_data': users_data})
def users(request):
    userdetails_file = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')
    paused_users_file = os.path.join(settings.BASE_DIR, 'UserDetails/paused_users.txt')

    paused_users = set()
    if os.path.exists(paused_users_file):
        with open(paused_users_file, 'r') as file:
            paused_users = {line.strip() for line in file if line.strip()}

    users_data = []
    if os.path.exists(userdetails_file):
        with open(userdetails_file, 'r') as file:
            for line in file:
                if line.strip():
                    try:
                        user_data = parse_user_line(line)
                        user_data['status'] = 'paused' if user_data['name'] in paused_users else user_data['status']
                        users_data.append(user_data)
                    except ValueError as e:
                        print(e)  # For debugging

    return render(request, 'users.html', {'users_data': users_data})


# def users(request):
#     userdetails_file = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')
#     paused_users_file = os.path.join(settings.BASE_DIR, 'UserDetails/paused_users.txt')

#     paused_users = set()
#     if os.path.exists(paused_users_file):
#         with open(paused_users_file, 'r') as file:
#             paused_users = {parse_user_line(line)['name'] for line in file if line.strip()}

#     users_data = []
#     if os.path.exists(userdetails_file):
#         with open(userdetails_file, 'r') as file:
#             for line in file:
#                 if line.strip():
#                     try:
#                         user_data = parse_user_line(line)
#                         user_data['status'] = 'paused' if user_data['name'] in paused_users else 'active'
#                         users_data.append(user_data)
#                     except ValueError as e:
#                         print(e)  # For debugging

#     return render(request, 'users.html', {'users_data': users_data})

def pause_resume_user(request, username):
    userdetails_file = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')
    paused_users_file = os.path.join(settings.BASE_DIR, 'UserDetails/paused_users.txt')

    # Read paused users
    paused_users = set()
    if os.path.exists(paused_users_file):
        with open(paused_users_file, 'r') as file:
            paused_users = {parse_user_line(line)['name'] for line in file if line.strip()}

    # Read userdetails
    user_lines = []
    if os.path.exists(userdetails_file):
        with open(userdetails_file, 'r') as file:
            user_lines = file.readlines()

    # Prepare to write back to userdetails and paused_users
    new_user_lines = []
    user_found = False
    for line in user_lines:
        if username in line:
            user_found = True
            if username in paused_users:
                # Resume the user: remove from paused_users and update status to active
                paused_users.remove(username)
                new_user_lines.append(line.replace('status: paused', 'status: active'))  # Update status to active
            else:
                # Pause the user: add to paused_users and update status to paused
                paused_users.add(username)
                new_user_lines.append(line.replace('status: active', 'status: paused'))  # Update status to paused
        else:
            new_user_lines.append(line)

    # Write updated userdetails
    with open(userdetails_file, 'w') as file:
        file.writelines(new_user_lines)

    # Write updated paused_users
    with open(paused_users_file, 'w') as file:
        file.writelines(f"{username}\n" for username in paused_users)

    return redirect('users')



def ai_key_view(request):
    ai_key = "sk-UmYT-NcN9RO2R7VaKbkEIFF0KTd1R0TLdVZfSY8lmGT3BlbkFJA3Ut8wKOUZUnbR4pVPqwonnRQqB-j11qd9F4twEsQA" 
    return render(request, 'ai_key.html', {'ai_key': ai_key})

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')  # Redirect to the article list after saving
    else:
        form = ArticleForm()
    
    return render(request, 'add_article.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def gpt_check_summary(article_url, summary):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": (
            f"The following is a user-submitted summary for the article at {article_url}:\n\n"
            f"Summary: '{summary}'\n\n"
            "Please evaluate the summary. Does it accurately reflect the content of the article based on its URL? "
            "If the summary is valid, respond with 'Valid summary'. If it is not valid, provide feedback on what "
            "needs improvement."
        )}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.5
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def load_articles_from_file(file_path):
    articles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        article = {}
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith('ArticleWebsite:'):
                    article['ArticleWebsite'] = line.split('ArticleWebsite: ', 1)[1] if len(line.split('ArticleWebsite: ', 1)) > 1 else 'Unknown'
                elif line.startswith('ArticleName:'):
                    article['ArticleName'] = line.split('ArticleName: ', 1)[1] if len(line.split('ArticleName: ', 1)) > 1 else 'Unknown'
                elif line.startswith('ArticleSummary:'):
                    article['ArticleSummary'] = line.split('ArticleSummary: ', 1)[1] if len(line.split('ArticleSummary: ', 1)) > 1 else 'Unknown'
                elif line.startswith('ArticleURL:'):
                    article['ArticleURL'] = line.split('ArticleURL: ', 1)[1] if len(line.split('ArticleURL: ', 1)) > 1 else 'Unknown'
                    if article:
                        articles.append(article)
                        article = {}
        # Handle the case where the last article might not have been appended
        if article:
            articles.append(article)
    return articles



def submit(request):
    articles = load_articles_from_file('UserDetails/articles.txt')
    
    if request.method == 'POST':
        article_url = request.POST.get('articleURL')
        userInput = request.POST.get('userInput')
        
        if article_url and userInput:
            # Find the article with the given URL
            article = next((a for a in articles if a.get('ArticleURL') == article_url), None)
            
            if article:
                gpt_response = gpt_check_summary(article_url, userInput)

                if gpt_response == 'Valid summary.':
                    return redirect('thankyou.html')
                else:
                    return render(request, 'submit.html', {
                        'articles': articles,
                        'error': gpt_response
                    })
            else:
                return redirect('thankyou')
                # return render(request, 'submit.html', {
                #     'articles': articles,
                #     'error': 'Article not found.'
                #})
        else:
            return render(request, 'submit.html', {
                'articles': articles,
                'error': 'Both article URL and summary are required.'
            })
    
    return render(request, 'submit.html', {'articles': articles})



# def submit(request):
#     articles = Article.objects.all()  # Fetch all articles from the database
    
#     if request.method == 'POST':
#         article_url = request.POST.get('articleURL')  # Fetch selected article URL
#         userInput = request.POST.get('userInput')  # Fetch the submitted summary
        
#         if article_url and userInput:
#             # Check the summary using GPT in reference to the article URL
#             gpt_response = gpt_check_summary(article_url, userInput)
#             print(gpt_response)
#             # Process GPT response
#             if gpt_response == 'Valid summary':
#                 return redirect('thankyou')  # Redirect to a 'thank you' page (ensure you have the view)
#             else:
#                 # If the GPT response gives feedback, re-render with the error
#                 return render(request, 'submit.html', {
#                     'articles': articles,
#                     'error': gpt_response
#                 })
#         else:
#             # If either field is missing, show an error message
#             return render(request, 'submit.html', {
#                 'articles': articles,
#                 'error': 'Both article URL and summary are required.'
#             })
    
#     # Render the form on a GET request
#     return render(request, 'submit.html', {'articles': articles})

def check_summary(request):
    error = None
    
    if request.method == 'POST':
        article_url = request.POST.get('articleURL')
        summary = request.POST.get('userInput')
        
        # Check if both fields are submitted
        if article_url and summary:
            # Call the GPT check function with the article URL and summary
            evaluation = gpt_check_summary(article_url, summary)
            return render(request, 'result.html', {'evaluation': evaluation})
        else:
            error = "Please select an article and provide a summary."
    
    articles = Article.objects.all()  # Fetch all articles for the dropdown
    return render(request, 'check_summary.html', {'articles': articles, 'error': error})


def thankyou(request):

    counter = SubmissionCount.objects.get(pk=1)
    counter.count += 1
    counter.save() 
    return render(request, 'thankyou.html', {'count': counter.count, 'late_count': counter.late_count})

# def register_view(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             #messages.success(request, 'Registration successful. You can now log in.')
#             return redirect('index.html')  # Redirect to the login page or another appropriate page
#     else:
#         form = RegistrationForm()
    
#     return render(request, 'registration.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mothers_email = request.POST.get('mothers_email')
        fathers_email = request.POST.get('fathers_email')

        # Automatically generate the username from the email (everything before @)
        username = email.split('@')[0]

        userdetails_file = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')

        # Check if the emails are filled or assign "None" if missing
        mothers_email = mothers_email if mothers_email else "None"
        fathers_email = fathers_email if fathers_email else "None"

        # Format the user details line
        user_line = f"Username: {username}, Email: {email}, Mother's Email: {mothers_email}, Father's Email: {fathers_email}, Status: active\n"

        # Append the new user details to userdetails.txt
        with open(userdetails_file, 'a') as file:
            file.write(user_line)

        return redirect('users')  # Redirect to the users page after registration

    return render(request, 'registration.html')



def email_list_view(request):
    emails = RegisteredEmail.objects.all()    
    return render(request, 'email_list.html', {'emails': emails})


def success_views(request):
    return render(request, 'success1.html')
                          
def options_view(request):
    return render(request, 'options.html')
    
def pause_registration_view(request, username):
    userdetails_file = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')

    # Read all user details
    with open(userdetails_file, 'r') as file:
        lines = file.readlines()

    # Update status in userdetails.txt
    with open(userdetails_file, 'w') as user_file:
        for line in lines:
            if f"Username: {username}" in line:
                # Update status to paused
                line = line.replace("Status: active", "Status: paused")
            user_file.write(line)

    return redirect('users')


def resume_registration_view(request, username):
    userdetails_file = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')

    # Read all user details
    with open(userdetails_file, 'r') as file:
        lines = file.readlines()

    # Update status in userdetails.txt
    with open(userdetails_file, 'w') as user_file:
        for line in lines:
            if f"Username: {username}" in line:
                # Update status to active
                line = line.replace("Status: paused", "Status: active")
            user_file.write(line)

    return redirect('users')




def pause_registration(user_name, user_email, mothers_email, fathers_email):
    # Define file paths
    user_file_path = os.path.join(settings.BASE_DIR, 'UserDetails', 'userdetails.txt')
    paused_file_path = os.path.join(settings.BASE_DIR, 'UserDetails', 'paused_users.txt')
    
    if os.path.exists(user_file_path):
        # Read all lines from the user details file
        with open(user_file_path, 'r') as file:
            lines = file.readlines()
        
        # Ensure paused_users.txt exists, create it if necessary
        if not os.path.exists(paused_file_path):
            open(paused_file_path, 'w').close()

        # Write all lines except the one with the matching user details to userdetails.txt
        # Write the matching line to paused_users.txt
        with open(user_file_path, 'w') as user_file, open(paused_file_path, 'a') as paused_file:
            for line in lines:
                if (user_name in line and user_email in line and 
                    mothers_email in line and fathers_email in line):
                    paused_file.write(f" Username: {user_name}, Email: {user_email}, Mother's Email: {mothers_email}, Father's Email: {fathers_email}, Status: paused\n")
                else:
                    user_file.write(line)


def remove_user_view(request, username):
    userdetails_file = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')

    if request.method == 'POST':
        # Read all user details
        if os.path.exists(userdetails_file):
            with open(userdetails_file, 'r') as file:
                lines = file.readlines()

            # Write back all lines except the one with the matching username
            with open(userdetails_file, 'w') as file:
                for line in lines:
                    if username not in line:
                        file.write(line)

    return redirect('users')

def article_view(request):
    articles = []
    article_file = os.path.join(settings.BASE_DIR, 'UserDetails', 'articles.txt')

    if os.path.exists(article_file):
        with open(article_file, 'r') as file:
            for line in file.readlines():
                article_data = {}
                parts = line.strip().split(', ')
                for part in parts:
                    key, value = part.split(': ')
                    article_data[key] = value
                articles.append(article_data)

    error = None
    if request.method == 'POST':
        user_input = request.POST.get('userInput')
        selected_article = request.POST.get('articleURL')

        # Perform word count validation or any other logic here
        word_count = len(user_input.split())
        if word_count > 20:
            error = 'Your input exceeds the 20-word limit. Please reduce the number of words.'

    return render(request, 'article_form.html', {'articles': articles, 'error': error})

def send_email(subject, body, to_emails):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    message = MIMEMultipart()
    message['From'] = smtp_user
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        for email in to_emails:
            message['To'] = email
            server.sendmail(smtp_user, email, message.as_string())
            print(f'Email sent to {email}')

def parse_user_details(file_path):
    emails = []
    with open(file_path, 'r') as file:
        for line in file:
            if 'Email:' in line:
                parts = line.split(',')
                for part in parts:
                    if 'Email:' in part:
                        email = part.split(':')[1].strip()
                        emails.append(email)
    return emails

def send_notification_emails(request):
    user_details_file = 'UserDetails/userdetails.txt'
    subject = 'Important Notification'
    body = 'This is a test email sent to all users listed in userdetails.txt.'

    emails = parse_user_details(user_details_file)
    if emails:
        send_email(subject, body, emails)
        return HttpResponse('Emails sent successfully.')
    else:
        return HttpResponse('No emails found to send.')
