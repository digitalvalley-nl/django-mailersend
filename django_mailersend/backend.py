# Python Standard Library
import base64
from email.mime.base import MIMEBase

# Django
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

# MailerSend
from mailersend.emails import NewEmail


class MailerSendEmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages):

        # Optionally load the api key from the Django settings
        mailersend_options = {}
        if hasattr(settings, 'MAILERSEND_API_KEY'):
            mailersend_options['mailersend_api_key'] = \
                settings.MAILERSEND_API_KEY

        # Iterate the email messages
        for email_message in email_messages:

            # Make sure the email does not contain any extra headers
            if len(email_message.extra_headers.keys()) > 0:
                raise ValueError('Extra headers not supported')

            # Make sure the main content type is supported
            mail_content = {}
            if email_message.content_subtype == 'plain':
                mail_content['text/plain'] = email_message.body
            elif email_message.content_subtype == 'html':
                mail_content['text/html'] = email_message.body
            else:
                raise ValueError('Content type not supported')

            # Make sure the alternative content type is supported, if present
            if hasattr(email_message, 'alternatives'):
                for alternative in email_message.alternatives:
                    if alternative[1] in ['text/html', 'text/plain']:
                        mail_content[alternative[1]] = alternative[0]
                    else:
                        raise ValueError('Content type not supported')

            # Prepare the email

            mailer = NewEmail(**mailersend_options)
            mail_body = {}

            # Set the mail content
            if 'text/plain' in mail_content:
                mailer.set_plaintext_content(
                    mail_content['text/plain'], mail_body)
            if 'text/html' in mail_content:
                mailer.set_html_content(mail_content['text/html'], mail_body)

            # Set the mail from
            mail_from = {'email': email_message.from_email}
            mailer.set_mail_from(mail_from, mail_body)

            # Set the mail to
            mail_to = list(
                map(
                    lambda to: {'email': to},
                    email_message.to
                )
            )
            mailer.set_mail_to(mail_to, mail_body)

            # Set the subject
            mailer.set_subject(email_message.subject, mail_body)

            # Optionally add the cc's
            if len(email_message.cc) > 0:
                mail_cc = list(
                    map(
                        lambda cc: {'email': cc},
                        email_message.cc
                    )
                )
                mailer.set_cc_recipients(mail_cc, mail_body)

            # Optionally add the bcc's
            if len(email_message.bcc) > 0:
                mail_bcc = list(
                    map(
                        lambda bcc: {'email': bcc},
                        email_message.bcc
                    )
                )
                mailer.set_bcc_recipients(mail_bcc, mail_body)

            # Optionally add the reply to
            if len(email_message.reply_to) > 0:
                mail_reply_to = list(
                    map(
                        lambda reply_to: {'email': reply_to},
                        email_message.reply_to
                    )
                )
                mailer.set_reply_to(mail_reply_to, mail_body)

            # Optionally add the attachments
            if len(email_message.attachments) > 0:
                mail_attachments = []
                for attachment in email_message.attachments:
                    if isinstance(attachment, MIMEBase):
                        filename = attachment.get_filename()
                        content = attachment.get_payload()
                    else:
                        filename = attachment[0]
                        content = attachment[1]
                    mail_attachments.append({
                        'id': filename,
                        'filename': filename,
                        'content': base64.b64encode(
                            bytes(content)).decode('ascii'),
                        'disposition': 'attachment'
                    })
                mailer.set_attachments(mail_attachments, mail_body)

            # Send the email
            mailer.send(mail_body)
