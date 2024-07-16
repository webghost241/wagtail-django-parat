from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from config import settings
from parat.core.models import AbstractBaseModel


class ContactRequest(AbstractBaseModel):
    name = models.CharField(
        max_length=64, blank=False, null=False, verbose_name=_("Name")
    )
    company = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("Unternehmen")
    )
    phone = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("Rufnummer")
    )
    email = models.EmailField(
        max_length=64, blank=False, null=False, verbose_name=_("E-Mail-Addresse")
    )
    message = models.TextField(blank=False, null=False, verbose_name=_("Nachricht"))
    dsgvo = models.BooleanField(
        blank=False,
        null=False,
        verbose_name=_("DSGVO"),
    )

    def send_notification_mails(self, request):
        # TODO: enable as soon as the spam crap has been taken care of
        # self.send_user_notification_mail(request)
        self.send_system_notification_mail(request)

    def send_user_notification_mail(self, request):
        lan = get_language()
        msg_html = render_to_string(
            f"mail/contact_form_confirmation_{lan}.html", {"request": request}
        )
        mst_text = strip_tags(msg_html)
        notification_mail = EmailMultiAlternatives(
            subject=_("Vielen Dank für ihre Anfrage"),
            to=[self.email],
            body=mst_text,
            from_email=settings.SERVER_EMAIL,
            reply_to=[settings.EMAIL_REPLYTO],
        )
        notification_mail.attach_alternative(msg_html, "text/html")
        notification_mail.send()

    def send_system_notification_mail(self, request):
        msg_html = render_to_string(
            "mail/contact_form_system_notification.html",
            {"contact_request": self, "request": request},
        )
        mst_text = strip_tags(msg_html)
        notification_mail = EmailMultiAlternatives(
            subject=_("Neue Kontaktanfrage von %(name)s, %(company)s")
            % {"name": self.name, "company": self.company},
            to=settings.NOTIFICATION_MAIL,
            body=mst_text,
            from_email=settings.SERVER_EMAIL,
            # reply_to=[settings.SERVER_EMAIL],
        )
        notification_mail.attach_alternative(msg_html, "text/html")
        notification_mail.send()
