from email.utils import formataddr
import random
import smtplib
from Users.models import Users
import re
import hashlib
import logging
from email.message import EmailMessage
import os
from django.core.mail import send_mail
'''
In this file there is all the helper function
for the User app and maybe others'''

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_SERVER = os.environ.get('EMAIL_SERVER')
FROM_EMAIL = os.environ.get('COMPANY_EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

def generate_random_digits() -> str:
    return ''.join(random.choice('0123456789') for _ in range(4))


def send_email(sender_email,receiver_email,message,subject) -> None:

    try:
        # Create the base text message.
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = formataddr(("Rent Share", f"{sender_email}"))
        msg["To"] = receiver_email

        msg.set_content(message)

        with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
            server.starttls()
            server.login(sender_email, EMAIL_PASSWORD)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        
        return None
    
    except Exception as e:
        logger.error('Error send email: %s', e)

def send_email_via_mailtrap(sender_email, receiver_email, message, subject) -> None:
    
    send_mail(subject="איפוס סיסמה",message=message,from_email=sender_email,recipient_list=[receiver_email])

def check_valid_password(pas:str) -> bool:

    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)' # contains at least one upper and one lower letter and number.

    return True if re.match(pattern,pas) and len(pas) >= 8 else False


def hash_password(plain_password:str) -> str:
    '''encrypt the password user using sha256 algorithm'''

    sha256 = hashlib.sha256()
    sha256.update(plain_password.encode('utf-8'))
    hashed_password = sha256.hexdigest()

    return hashed_password


def email_exists(email:str) -> bool:
    '''exists() method returns True if user_email already in the db'''

    return Users.objects.filter(user_email=email).exists()


def phone_exists(phone:str)-> bool:
    '''returns True if at least one record matches the filter, and False if no records match.'''

    return Users.objects.filter(user_phone=phone).exists()


def full_name_check(full_name:str) -> bool:
    '''
    check if the full name is valid
    full name must be at least 4 characters and contain at least one space.
    '''

    space_place = full_name.find(' ') # to ensure that there is a space in the full name
    return True if len(full_name) >= 3 and space_place != -1 and len(full_name[space_place:]) > 0 else False


def phone_number_check(phone_number:str) -> bool:
    '''
    check if the phone number is valid.
    phone number must be at least 10 characters.    
    '''

    return True if len(phone_number) == 10 and phone_number.isdigit() else False


def check_email_valid(email:str)-> bool:
    '''in registration, the email is checked by Django but when he change it we need to check it again'''
    return True if email.count('@') == 1 and email.count('.') >= 1 else False