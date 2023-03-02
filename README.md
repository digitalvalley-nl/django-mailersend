# Django MailerSend

Django MailerSend makes it easier to send emails in Django apps using the
MailerSend API. Uses the official MailerSend Python SDK internally.

## Index

- Installation
- Configuration
- Usage
  - Text Only Emails
  - Text + HTML Emails
  - Attachments

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

### Text Only Emails

- Send a **Text Only** email using Django's `send_mail` function:

```python
from django.core.mail import send_mail

send_mail(
  subject='Hello world!',
  message='Sent using the Django MailerSend Email Backend!',
  from_email='sender@example.com',
  recipient_list=['receiver@example.com']
)
```

- Send a **Text Only** email using Django's `EmailMessage` class for more options:

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

### Text + HTML Emails

- Send a **Text + HTML** email using Django's `send_mail` function:

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

- Send a **Text + HTML** email using Django's `EmailMultiAlternatives` class for more
options:

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

### Attachments

Sending attachments is supported when using Django's `EmailMessage` or
`EmailMultiAlternatives` classes. There are several ways of doing this:

- Send an attachment by providing the file `path` to the `attach_file` method:

```python
from django.core.mail.message import EmailMessage

email_message = EmailMessage(
  subject='Hello world!',
  body='Sent using the Django MailerSend Email Backend!',
  from_email='sender@example.com',
  to=['receiver@example.com']
)
email_message.attach_file('/example/attachment.txt')
email_message.attach_file('/example/attachment.jpg')
email_message.send()
```

- Send an attachment by providing a `filename` and the file `content` to the `attach` method:

```python
from django.core.mail.message import EmailMessage

email_message = EmailMessage(
  subject='Hello world!',
  body='Sent using the Django MailerSend Email Backend!',
  from_email='sender@example.com',
  to=['receiver@example.com']
)

# Text file (Read mode 'r')
with open('/example/attachment.txt', 'r') as file:
    email_message.attach('attachment.txt', file.read())

# Binary file (Read mode 'rb')
with open('/example/attachment.jpg', 'rb') as file:
    email_message.attach('attachment.jpg', file.read())

email_message.send()
```

- Send an attachment by providing a `MIMEBase` instance to the `attach` method:

```python
from django.core.mail.message import EmailMessage

email_message = EmailMessage(
  subject='Hello world!',
  body='Sent using the Django MailerSend Email Backend!',
  from_email='sender@example.com',
  to=['receiver@example.com']
)

# Text file (Read mode 'r')
with open('/example/attachment.txt', 'r') as file:
    mime_text = MIMEText(file.read())
    mime_text.add_header(
      'Content-Disposition', 'attachment; filename=attachment.txt')
    email_message.attach(mime_text)

# Binary file (Read mode 'rb')
with open('/example/attachment.jpg', 'rb') as file:
    mime_image = MIMEImage(file.read())
    mime_image.add_header(
      'Content-Disposition', 'inline; filename=attachment.jpg')
    email_message.attach(mime_image)

email_message.send()
```

## Resources

- Django: https://www.djangoproject.com/
- MailerSend: https://www.mailersend.com/
- MailerSend Python SDK: https://github.com/mailersend/mailersend-python
