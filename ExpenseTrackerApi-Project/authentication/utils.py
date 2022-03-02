from django.core.mail import EmailMessage
import pdb

class Util:

    @staticmethod
    def send_email(data):
        # pdb.set_trace()
        email=EmailMessage(subject=data['email_subject'],body=data['email_body'],to=[data['to_email']])
        email.send()
