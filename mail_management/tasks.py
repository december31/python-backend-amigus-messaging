import logging
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import shared_task
from django.utils import timezone

from mail_management.models import MailLog
from project import settings

logger = logging.getLogger(__name__)

@shared_task
def send_mail_async(mail_id: int):
    mail_log = MailLog.objects.get(id=mail_id)

    try:
        mail_host = settings.EMAIL_HOST
        mail_port = settings.EMAIL_PORT
        mail_host_user = settings.EMAIL_HOST_USER
        mail_host_password = settings.EMAIL_HOST_PASSWORD
        use_tls = settings.EMAIL_USE_TLS

        mail_server = smtplib.SMTP(mail_host, mail_port)
        if use_tls:
            mail_server.starttls()
        mail_server.login(mail_host_user, mail_host_password)

        html_message = mail_log.content

        msg = MIMEMultipart()
        msg['From'] = mail_host_user
        msg['To'] = mail_log.receiver
        msg['Subject'] = mail_log.subject

        # Attach the body of the email
        msg.attach(MIMEText(html_message, 'html'))

        mail_server.sendmail(
            from_addr=mail_host_user,
            to_addrs=[mail_log.receiver],
            msg=msg.as_string()
        )

        mail_log.status = MailLog.StatusChoice.SUCCESS.value
        mail_log.sent_at = timezone.now()
        mail_log.save()

    except Exception as e:
        mail_log.status = MailLog.StatusChoice.FAILURE.value
        mail_log.error_message = traceback.format_exc()
        mail_log.save()
        traceback.print_exc()
