from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from parat.contact.forms import ContactForm
from parat.core.models.wagtail import AbstractStandardPage


class ContactPage(AbstractStandardPage):
    contact_information = RichTextField(verbose_name=_("Kontaktinformationen"))
    form_header = RichTextField(verbose_name=_("Formularkopf"))

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(form=ContactForm())
        return context

    def serve(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save_and_send_out_mails(request)
                messages.success(
                    #request, _("Ihre Nachricht wurde erfolgreich versendet")
                    request, _("Ihre Nachricht wurde erfolgreich versendet / Your Message was successfully sent")
                )
            else:
                context["form"] = form
        return TemplateResponse(
            request=request,
            template=self.get_template(request, *args, **kwargs),
            context=context,
        )

    content_panels = AbstractStandardPage.content_panels + [
        FieldPanel("contact_information"),
        FieldPanel("form_header"),
    ]
