import threading
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from twilio.rest import Client

# Threading
class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()

class SMSThread(threading.Thread):
    def __init__(self, message,recipient):
        self.message = message
        self.recipient = recipient
        threading.Thread.__init__(self)
    def run(self):
        client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
        phone_number = settings.TWILIO_DEFAULT_CALLERID
        for phone in self.recipient:
            client.messages.create(from_=phone_number,body=self.message,to=phone)



def send_mail(subject, message, recipient):
    from_email = settings.EMAIL_HOST_USER
    if type(recipient) == list:
        recipient_list = recipient
    else:
        recipient_list = [recipient]

    try:
        e_message = EmailMessage(subject, message, from_email, recipient_list)
        e_message.content_subtype = 'html'
        EmailThread(e_message).start()
    except Exception as e:
        print(e)
        pass


def send_message( message, recipient):
    SMSThread(message,recipient).start()


    


