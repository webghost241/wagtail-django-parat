from rest_framework.routers import SimpleRouter, DefaultRouter
from django.conf import settings

# from parat.core.api import VersionViewSet

router = None

# when DEBUG mode is enabled, allow API listing
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

#
# Register your API routes below
#

# router.register(r'version', VersionViewSet, basename='version)
