# import openai
# from django.conf import settings

# openai.api_key = settings.OPENAI_API_KEY

# def gpt_check_summary(summary):
#     prompt = (
#         f"The following is a user-submitted summary: '{summary}'.\n"
#         "Please check if the summary is appropriate and within 20 words. "
#         "If the summary is appropriate and concise, respond with 'Valid summary'. "
#         "Otherwise, provide feedback on what could be improved or if the summary is too long."
#     )
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # Use the appropriate engine
#         prompt=prompt,
#         max_tokens=50
#     )
#     return response['choices'][0]['text'].strip()

# import openai
# from django.conf import settings

# openai.api_key = settings.OPENAI_API_KEY

# def gpt_check_summary(article, summary):
#     prompt = (
#         f"The following is an article: '{article}'\n"
#         f"The following is a user-submitted summary of the article: '{summary}'\n"
#         "Please check if the summary is appropriate and concise (up to 20 words). "
#         "If the summary is valid and meets the criteria, respond with 'Valid summary'. "
#         "If it is not valid, provide feedback on what needs improvement or if the summary is too long."
#     )
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # Use the appropriate engine
#         prompt=prompt,
#         max_tokens=100  # Adjust as needed
#     )
#     return response['choices'][0]['text'].strip()


import openai
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import logging
import os

logger = logging.getLogger(__name__)

# Ensure the API key is set
try:
    openai.api_key = settings.OPENAI_API_KEY
except AttributeError:
    raise ImproperlyConfigured("OPENAI_API_KEY is not set in Django settings")
    

def gpt_check_summary(article, summary):
    prompt = (
        f"The following is an article:\n\n'{article}'\n\n"
        f"The following is a user-submitted summary of the article:\n\n'{summary}'\n\n"
        "Please evaluate the summary. Is it accurate and does it concisely cover the main points of the article? "
        "If the summary is valid and meets the criteria, respond with 'Valid summary'. "
        "If it is not valid, provide feedback on what needs improvement."
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate engine
            prompt=prompt,
            max_tokens=100,  # Adjust based on expected response length
            temperature=0.5,  # Lower temperature for more deterministic responses
            n=1  # Generate a single response
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"Error with OpenAI API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


# def pause_registration(user_name, user_email, parent_email):
#     # Define file paths
#     user_file_path = os.path.join(settings.BASE_DIR, 'UserDetails', 'userdetails.txt')
#     paused_file_path = os.path.join(settings.BASE_DIR, 'UserDetails', 'paused_users.txt')
#     temp_file_path = user_file_path + '.tmp'
    
#     # Ensure paused_users.txt exists and create it if necessary
#     if not os.path.exists(paused_file_path):
#         try:
#             with open(paused_file_path, 'w') as paused_file:
#                 # Create an empty file
#                 print(f"Creating file: {paused_file_path}")
#                 paused_file.write('')
#         except Exception as e:
#             print(f"Error creating paused_users.txt: {e}")
    
#     # Process the userdetails file
#     if os.path.exists(user_file_path):
#         try:
#             with open(user_file_path, 'r') as file, open(temp_file_path, 'w') as temp_file:
#                 with open(paused_file_path, 'a') as paused_file:
#                     for line in file:
#                         # Debug output to check the line being processed
#                         print(f"Processing line: {line.strip()}")
                        
#                         # If the line matches the user details, append it to paused_users.txt
#                         if user_name in line and user_email in line and parent_email in line:
#                             print(f"Pausing: {line.strip()}")
#                             paused_file.write(line)  # Write to paused_users.txt
#                         else:
#                             temp_file.write(line)  # Write to temporary file
#             # Replace the original file with the updated temp file
#             os.replace(temp_file_path, user_file_path)
#         except Exception as e:
#             print(f"Error processing files: {e}")

# def resume_registration(user_name, user_email, parent_email):
#     user_file_path = os.path.join(settings.BASE_DIR, 'UserDetails/userdetails.txt')
#     paused_file_path = os.path.join(settings.BASE_DIR, 'UserDetails/paused_users.txt')
#     temp_file_path = paused_file_path + '.tmp'
    
#     # Process the paused_users file
#     if os.path.exists(paused_file_path):
#         with open(paused_file_path, 'r') as paused_file, open(temp_file_path, 'w') as temp_file:
#             with open(user_file_path, 'a') as user_file:
#                 for line in paused_file:
#                     if user_name in line and user_email in line and parent_email in line:
#                         user_file.write(line)  # Append to userdetails.txt
#                     else:
#                         temp_file.write(line)  # Write to temp file
#         os.replace(temp_file_path, paused_file_path)

def pause_registration(user_name, user_email, parent_email):
    # Define file paths
    user_file_path = os.path.join(settings.BASE_DIR, 'UserDetails', 'userdetails.txt')
    paused_file_path = os.path.join(settings.BASE_DIR, 'UserDetails', 'paused_users.txt')
    temp_file_path = user_file_path + '.tmp'
    
    # Ensure paused_users.txt exists and create it if necessary
    if not os.path.exists(paused_file_path):
        try:
            with open(paused_file_path, 'w') as paused_file:
                paused_file.write('')
            print(f"Paused users file created: {paused_file_path}")
        except Exception as e:
            print(f"Error creating paused_users.txt: {e}")

    # Check if the user file exists
    if os.path.exists(user_file_path):
        try:
            with open(user_file_path, 'r') as file, open(temp_file_path, 'w') as temp_file:
                with open(paused_file_path, 'a') as paused_file:
                    for line in file:
                        # Debug output to check the line being processed
                        print(f"Processing line: {line.strip()}")
                        
                        # If the line matches the user details, append it to paused_users.txt
                        if user_name in line and user_email in line and parent_email in line:
                            print(f"Pausing user: {line.strip()}")
                            paused_file.write(line)  # Write to paused_users.txt
                        else:
                            temp_file.write(line)  # Write to temporary file
            # Replace the original file with the updated temp file
            os.replace(temp_file_path, user_file_path)
        except Exception as e:
            print(f"Error processing files: {e}")

def resume_registration(user_name, user_email, parent_email):
    # Define file paths
    user_file_path = os.path.join(settings.BASE_DIR, 'UserDetails', 'userdetails.txt')
    paused_file_path = os.path.join(settings.BASE_DIR, 'UserDetails', 'paused_users.txt')
    temp_file_path = paused_file_path + '.tmp'
    
    # Check if the paused users file exists
    if os.path.exists(paused_file_path):
        try:
            with open(paused_file_path, 'r') as paused_file, open(temp_file_path, 'w') as temp_file:
                with open(user_file_path, 'a') as user_file:
                    for line in paused_file:
                        # Debug output to check the line being processed
                        print(f"Processing line: {line.strip()}")
                        
                        # If the line matches the user details, restore it to userdetails.txt
                        if user_name in line and user_email in line and parent_email in line:
                            print(f"Restoring user: {line.strip()}")
                            user_file.write(line)  # Write to userdetails.txt
                        else:
                            temp_file.write(line)  # Write to temporary file
            # Replace the paused users file with the updated temp file
            os.replace(temp_file_path, paused_file_path)
        except Exception as e:
            print(f"Error processing files: {e}")

            