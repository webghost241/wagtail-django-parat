from logging import getLogger

import requests
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from parat.contact.models.models import ContactRequest
from parat.core.templatetags.page_type_url import page_type_url

logger = getLogger(__name__)


class ContactForm(forms.ModelForm):
    spam = True

    helper = FormHelper()
    helper.layout = Layout(
        FloatingField("name", css_class="form-control rounded-pill"),
        FloatingField("company", css_class="form-control rounded-pill "),
        FloatingField("phone", css_class="form-control rounded-pill "),
        FloatingField("email", css_class="form-control rounded-pill "),
        FloatingField("message", css_class="form-control kontakt-form-textarea"),
        Field("dsgvo"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False
        self.fields["dsgvo"].required = True
        # self.fields["message"].widget.attrs["size"] = 10
        self.fields["message"].widget.attrs["style"] = "height: 100px"
        # print(self.fields["message"].widget)
        terms_and_conditions = page_type_url({}, "core", "DataProtectionPage").url
        self.fields["dsgvo"].label = mark_safe(
            _(
                'Ich stimme der Datenverarbeitung gemäß unserer <a target="_new" href="%(url)s">Datenschutzerklärung</a> zu'
            )
            % {"url": terms_and_conditions}
        )

        for f in self.fields:
            field = self.fields[f]
            if field in ["name", "company", "phone", "email", "message"]:
                field.widget.attrs["placeholder"] = field.label

    class Meta:
        model = ContactRequest
        fields = ["name", "company", "phone", "email", "message", "dsgvo"]
        labels = {
            "name": _("Name"),
            "company": _("Unternehmen"),
            "phone": _("Rufnummer"),
            "email": _("E-Mail-Adresse"),
            "message": _("Nachricht"),
        }

    def clean(self):
        cleaned_data = super().clean()
        try:
            post_parameter_key = "cf-captcha-response"
            if post_parameter_key in self.data:
                response_token = self.data[post_parameter_key]
                data = {
                    "secret": settings.FRIENDLY_CAPTCHA_API_KEY,
                    "response": response_token,
                }

                logger.info(f"Response Token '{response_token}'")

                response = requests.post(
                    "https://api.captchafox.com/siteverify",
                    data=data,
                )

                data = response.json()

                logger.info(f"Riddle response {data}")

                if data.get("success", False):
                    logger.info("Riddle completed successfully, assuming legit")
                    self.spam = False
                else:
                    logger.info("Riddle not completed successfully, assuming SPAM.")
                    logger.info(f"Error Codes: {data.get('error-codes')}")
                    self.spam = True
            else:
                logger.info(f"No {post_parameter_key} data, assuming SPAM")
                self.spam = True
        except Exception as e:
            logger.error("Error while verifying spam, assuming spam", exc_info=e)
            self.spam = True

        return cleaned_data

    def save(self, commit=True):
        obj: ContactRequest = super().save(commit)
        return obj

    def save_and_send_out_mails(self, request):
        if self.spam:
            logger.info(
                f"Spam detected ({self.spam}) for {self.data}, not storing data, not sending E-Mail"
            )
            return None
        else:
            logger.info(
                f"NO Spam detected ({self.spam}) for {self.data}, storing data, sending E-Mail"
            )

            obj = self.save()
            logger.info("Sending out mails!")
            obj.send_notification_mails(request=request)
            return obj
