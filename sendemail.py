import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import requests

load_dotenv()


# Function to fetch email recipients from Google Sheet
def fetch_email_recipients():
    url = os.getenv('GOOGLE_SHEET_URL')  
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get('data', []) 
        email_receiver = [entry['email'] for entry in data]  
        return email_receiver
    else:
        print(f"Failed to fetch email recipients. Status code: {response.status_code}")
        return []

# Defining email sender and receiver
email_sender = 'nishanbaral987@gmail.com'
email_password = os.getenv('MY_PASSWORD')


# Fetch email recipients from Google Sheet
email_receiver = fetch_email_recipients()

# Set the subject and body of the email
subject = 'Check out my new video!'
body = """
What ever you write here
"""

# Add SSL (layer of security)
context = ssl.create_default_context()

# Loop through each recipient and send individual emails
for receiver_email in email_receiver:
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver_email, em.as_string())
        print(f"Email sent to {receiver_email}")


print("All emails sent.")
