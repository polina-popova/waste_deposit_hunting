import os
from email.mime.image import MIMEImage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_deposit_hunting.settings')
import django
django.setup()

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from reports.models import Report


def send_daily_report():
    unsent_reports = Report.objects.exclude(was_sent=True)
    to_be_sent_reports = [
        report for report in unsent_reports if os.path.isfile(report.photo.path)
    ]

    context = {'reports': to_be_sent_reports}
    html_content = render_to_string('email.html', context=context).strip()

    subject = settings.EMAIL_TITLE
    recipients = settings.EMAIL_RECEIVERS
    reply_to = settings.EMAIL_HOST_USER

    msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, recipients, reply_to=[reply_to])
    msg.content_subtype = 'html'  # Main content is text/html
    msg.mixed_subtype = 'related'
    msg.attach_alternative(html_content, "text/html")

    for to_be_sent_report in to_be_sent_reports:
        # Create an inline attachment
        try:
            image = MIMEImage(to_be_sent_report.photo.read())
        except FileNotFoundError:
            continue
        image.add_header('Content-ID', '<{}>'.format(to_be_sent_report.image_filename))
        msg.attach(image)

    msg.send()

    unsent_reports\
        .filter(pk__in=tuple(map(lambda x: x.pk, to_be_sent_reports)))\
        .update(was_sent=True)


if __name__ == '__main__':
    send_daily_report()
