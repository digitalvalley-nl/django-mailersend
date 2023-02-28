# Django
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend

# Requests
import requests


class MailerSendEmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages):

        # Iterate the email messages
        for email_message in email_messages:

            # Make sure the email does not contain attachments
            if len(email_message.attachments) > 0:
                raise ValueError('Attachments not supported')

            # Make sure the email does not contain multiple reply to's
            if len(email_message.reply_to) > 1:
                raise ValueError("Multiple reply to's not supported")

            # Make sure the email does not contain any extra headers
            if len(email_message.extra_headers.keys()) > 0:
                raise ValueError('Extra headers not supported')

            # Prepare the email base data
            data = {
                'from': {
                    'email': email_message.from_email,
                },
                'to': list(
                    map(
                        lambda to: {
                            'email': to
                        },
                        email_message.to
                    )
                ),
                'subject': email_message.subject
            }

            # Optionally add the cc's
            if len(email_message.cc) > 0:
                data['cc'] = list(
                    map(
                        lambda cc: {
                            'email': cc
                        },
                        email_message.cc
                    )
                )

            # Optionally add the bcc's
            if len(email_message.bcc) > 0:
                data['bcc'] = list(
                    map(
                        lambda bcc: {
                            'email': bcc
                        },
                        email_message.bcc
                    )
                )

            # Optionally add the reply to
            if len(email_message.reply_to) == 1:
                data['reply_to'] = {
                    'email': email_message.reply_to[0]
                }

            # If the email is multipart with text and html parts
            if isinstance(email_message, EmailMultiAlternatives) \
                    and email_message.content_subtype == 'plain' \
                    and len(email_message.alternatives) == 1 \
                    and email_message.alternatives[0][1] == 'text/html':
                data['text'] = email_message.body
                data['html'] = email_message.alternatives[0][0]

            # If the email is html only
            elif email_message.content_subtype == 'html':
                data['html'] = email_message.body

            # If the email is text only
            elif email_message.content_subtype == 'plain':
                data['text'] = email_message.body

            # Otherwise, the email is not supported
            else:
                raise ValueError('Content type not supported')

            # Send the email
            requests.post(
                url='https://api.mailersend.com/v1/email',
                headers={
                    'Authorization': 'Bearer ' + settings.MAILERSEND_API_TOKEN
                },
                json=data
            )
