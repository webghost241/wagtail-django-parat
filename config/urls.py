from core.api import get_version
from django.conf import settings

# django i18n is enabled by default
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from puput import urls as puput_urls
from rest_framework.authtoken.views import obtain_auth_token
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_transfer import urls as wagtailtransfer_urls

from config.api_router import router
from parat.core.api import get_font, get_version

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("cookies/", include("cookie_consent.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# API URLs
urlpatterns += [
    # API ViewSet Routes
    path("api/", include(router.urls)),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    #
    # Non ViewSet Routes
    #
    path("api/version/", get_version),
    path("api/font/", get_font),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

if settings.DEBUG_TOOLBAR:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

# Wagtail
urlpatterns += [
    # must be above all wagtail_urls
    path("wagtail-transfer/", include(wagtailtransfer_urls)),
    # not certain if adding puput urls to cms
    # and documents is actually necessary
    path("cms/", include(puput_urls)),
    path("documents/", include(puput_urls)),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]

# django i18n is enabled by default
urlpatterns += i18n_patterns(
    path("pages/", include(puput_urls)),
    path("", include(wagtail_urls)),
    prefix_default_language=False,
)
