from rest_framework.renderers import JSONRenderer


class VendorMimeTypeAPIRenderer(JSONRenderer):
    media_type = "application/vnd.parat+json"
