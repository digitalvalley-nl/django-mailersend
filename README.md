# Django MailerSend

Django MailerSend makes it easier to send emails in Django apps using the
MailerSend API.

## Installation

```
pip install django-mailersend
```

## Configuration

Add the following to your Django settings:
```
EMAIL_BACKEND = 'django_mailersend.backend.MailerSendEmailBackend'
MAILERSEND_API_KEY = 'Your API key'
```

## Usage

Send a text only email using Django's `send_mail` function:
```python
from django.core.mail import send_mail

send_mail(
  subject='Hello world!',
  message='Sent using the Django MailerSend Email Backend!',
  from_email='sender@example.com',
  recipient_list=['receiver@example.com']
)
```

Send a text + HTML email using Django's `send_mail` function:
```python
from django.core.mail import send_mail

send_mail(
  subject='Hello world!',
  message='Sent using the Django MailerSend Email Backend!',
  from_email='sender@example.com',
  recipient_list=['receiver@example.com'],
  html_message='<p>Sent using <strong>Django MailerSend Email Backend</strong>!</p>'
)
```

Send a text only email using Django's `EmailMessage` class for more options:
```python
from django.core.mail.message import EmailMessage

email_message = EmailMessage(
  subject='Hello world!',
  body='Sent using the Django MailerSend Email Backend!',
  from_email='sender@example.com',
  to=['receiver@example.com'],
  bcc=['bcc@example.com'], # Optional
  cc=['cc@example.com'], # Optional
  reply_to=['reply-to@example.com'] # Optional
)
email_message.send()
```

Send a text + HTML email using Django's `EmailMultiAlternatives` class for more options:
```python
from django.core.mail.message import EmailMultiAlternatives

email_message = EmailMultiAlternatives(
  subject='Hello world!',
  body='Sent using Django MailerSend Email Backend!',
  from_email='sender@example.com',
  to=['receiver@example.com'],
  bcc=['bcc@example.com'], # Optional
  cc=['cc@example.com'], # Optional
  reply_to=['reply-to@example.com'] # Optional
)
email_message.attach_alternative(
    '<p>Sent using <strong>Django MailerSend Email Backend</strong>!</p>',
    'text/html'
)
email_message.send()
```

You can also add attachments when using Django's `EmailMessage` or `EmailMultiAlternatives` classes:
```python
from django.core.mail.message import EmailMessage

# Attach a file using a file path
email_message = EmailMessage(
  subject='Hello world!',
  body='Sent using the Django MailerSend Email Backend!',
  from_email='sender@example.com',
  to=['receiver@example.com']
)
email_message.attach_file('/example/attachment.pdf')
email_message.send()

# Attach a file using a filename and the file content
email_message = EmailMessage(
  subject='Hello world!',
  body='Sent using the Django MailerSend Email Backend!',
  from_email='sender@example.com',
  to=['receiver@example.com']
)
with open('/example/attachment.pdf', 'rb') as file:
    file_content = file.read()
    email_message.attach('attachment.pdf', file_content)
email_message.send()
```

## Resources

- Django: https://www.djangoproject.com/
- MailerSend: https://www.mailersend.com/
