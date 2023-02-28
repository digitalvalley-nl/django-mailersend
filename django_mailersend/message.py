# Django
from django.core.mail import EmailMessage


class HTMLEmailMessage(EmailMessage):
    content_subtype = 'html'
