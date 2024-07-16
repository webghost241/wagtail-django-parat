from django.template import Library

register = Library()


@register.inclusion_tag("tags/breadcrubs.html", takes_context=True)
def breadcrumbs(context):
    return {"page": context["page"]}
