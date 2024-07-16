import os
import secrets
import sys
import urllib.parse
from pathlib import Path
from typing import List, Literal, Union

import dj_database_url
import django_cache_url
from pydantic import AnyUrl, BaseSettings, EmailStr, Field, NameEmail, PositiveInt

from parat import __api_version__

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# parat/
APPS_DIR = BASE_DIR / "parat"


class CacheBackendUrl(AnyUrl):
    host_required = False
    allowed_schemes = django_cache_url.BACKENDS.keys()


class ImplicitHostname(AnyUrl):
    host_required = False


class MediaBackendUrl(AnyUrl):
    host_required = False
    allowed_schemes = {"s3", "local"}


def as_bool(v: Union[str, list[str], None]):
    if v is None:
        return False

    if isinstance(v, str):
        v = [v]

    return v[0].lower() in ("true", "yes", "t", "1")


Environments = Literal["development", "staging", "production", "test"]
DJANGO_ENV_FILE = os.environ.get(
    "DJANGO_ENV_FILE", "test.env" if "pytest" in sys.modules else ".env"
)


class Settings(BaseSettings):
    """
    Pydantic-powered settings, to provide consistent error messages, strong
    typing, consistent prefixes, .venv support, etc.
    """

    #: The default database.
    DATABASE_URL: Union[ImplicitHostname, None]

    #: the currently running environment
    ENVIRONMENT: Environments = "development"

    #: Should django run in debug mode?
    DEBUG: bool = False

    #: Should the debug toolbar be loaded?
    DEBUG_TOOLBAR: bool = False

    #: Set a secret key used for signing values such as sessions. Randomized
    #: by default, so you'll logout everytime the process restarts
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_hex(128))

    #: If set, a list of allowed values for the HOST header. The default value
    #: of '*' means any host will be accepted.
    ALLOWED_HOSTS: list[str] = Field(default_factory=lambda: ["*"])

    # If set, a list of hosts to accept for CORS.
    CORS_HOSTS: list[str] = Field(default_factory=list)

    #: If set, a list of hosts to accept for CSRF.
    # Contrary to the name of the variable, each
    # HOST must be specified as a URL as of Django 4.0
    CSRF_HOSTS: list[str] = Field(default_factory=list)

    #: If enabled, trust the HTTP_X_FORWARDED_FOR header.
    USE_PROXY_HEADERS: bool = False

    #: Fallback domain for links
    MAIN_DOMAIN: str = "parat.de"

    EMAIL_SERVER: AnyUrl = "console://localhost"
    EMAIL_FROM: NameEmail = "PARAT Solutions <noreply@parat.de>"
    EMAIL_REPLYTO: EmailStr = "info@parat.de"
    AUTO_ADMIN_EMAIL: Union[EmailStr, None] = None
    ERROR_EMAILS: Union[list[EmailStr], None] = None
    NOTIFICATION_MAIL: List[EmailStr] = [
        "info@parat.de",
    ]

    MEDIA_URL: str = "/media/"
    MEDIA_ROOT: str = os.path.join(BASE_DIR, "media")
    MEDIA_BACKEND: Union[MediaBackendUrl, None] = None

    #: S3 ACL to apply to all media objects when MEDIA_BACKEND is set to S3. If using a CDN
    #: and/or have public access blocked to buckets this will likely need to be 'private
    MEDIA_BACKEND_S3_ACL: str = "public-read"

    #: Default cache backend
    CACHES_DEFAULT: Union[CacheBackendUrl, None] = None
    #: Wagtail
    WAGTAILADMIN_BASE_URL: str = "parat.de"

    # The secret key of this instance to that other instances must use to access data of this instance.
    WAGTAILTRANSFER_SECRET_KEY: str = "DummyKey"

    # The key of the correspondent stage
    WAGTAILTRANSFER_STAGE_KEY: str = "DummyKey"

    VITE_DEV_MODE: bool = False

    CRYPTOGRAPHY_ARGON2_TIMECOST: PositiveInt = 1
    CRYPTOGRAPHY_ARGON2_MEMORYCOST: PositiveInt = 2**20  # KiB
    CRYPTOGRAPHY_ARGON2_NPROC: PositiveInt = 8  # os.sysconf('SC_NPROCESSORS_ONLN')

    FRIENDLY_CAPTCHA_API_KEY: str = "empty"

    class Config:
        env_prefix = "DJANGO_"
        env_file = str(BASE_DIR / DJANGO_ENV_FILE)
        env_file_encoding = "utf-8"


SETUP = Settings()

SECRET_KEY = SETUP.SECRET_KEY
DEBUG = SETUP.DEBUG
DEBUG_TOOLBAR = SETUP.DEBUG_TOOLBAR



import colorful.fields

INSTALLED_APPS = [
    # parat
    "parat.jobs",
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # enables sync between wagtail instances
    "wagtail_transfer",
    "wagtail_modeladmin",          # if Wagtail >=5.1; Don't repeat if it's there already
    # "wagtail.contrib.modeladmin",  # if Wagtail <5.1;  Don't repeat if it's there already
    "wagtailmenus",
    # when using Wagtail, enhanced i18n is enabled by default
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtail_localize.modeladmin",
    "wagtail.contrib.simple_translation",
    "wagtail_trash",
    "modelcluster",
    "taggit",
    "crispy_forms",
    # health checks
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.psutil",
    # "health_check.contrib.celery",
    # "health_check.contrib.celery_ping",
    # "health_check.contrib.s3boto3_storage",
    # "health_check.contrib.rabbitmq",
    # "health_check.contrib.redis",
    "crispy_bootstrap5",
    "django_browser_reload",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
    "drf_standardized_errors",
    # local
    "parat.users",
    "parat.core",
    "parat.company",
    "parat.expo",
    "parat.solutions",
    "parat.downloads",
    "parat.contact",
    "parat.footer",
    "parat.news",
    # puput
    "wagtail.contrib.sitemaps",
    "wagtail.contrib.routable_page",
    "django_social_share",
    # SEO
    "wagtail.contrib.settings",
    "wagtailseo",
    "puput",
    "colorful",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # django i18n is enabled by default
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    # must be last
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]
REST_FRAMEWORK = {
    # per default, AcceptHeaderVersioning is used, see core.renderers.VendorMimeTypeAPIRenderer for more detail on how to provide the proper
    # MimeType
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.AcceptHeaderVersioning",
    # The default API version to be used if no version has been specified by the API consume
    "DEFAULT_VERSION": "1.0.0",
    # A list featuring supported API versions, if an API consumer attempts to use an invalid API version, a 406 is returned.
    "ALLOWED_VERSIONS": ["1.0.0"],
    # The header parameter used to transport the version, e.g. "Accept: application/vnd.sphericalelephant+json; version=1.0.0"
    "VERSION_PARAM": "version",
    # API renderers
    "DEFAULT_RENDERER_CLASSES": [
        # Custom vnd mime type API version renderer
        "parat.core.renderers.VendorMimeTypeAPIRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    # OpenAPI Spec, using the AutoSchema implementation of drf_standardized_errors. If you want to customize the schema class, you need to
    # extend drf_standardized_errors.openapi.AutoSchema
    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",
    # Using drf-standardized errors to handle exceptions and provide a consistent solution.
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
}

SPECTACULAR_SETTINGS = {
    # these mappings are required for drf_standardized_errors
    "ENUM_NAME_OVERRIDES": {
        "ValidationErrorEnum": "drf_standardized_errors.openapi_serializers.ValidationErrorEnum.values",
        "ClientErrorEnum": "drf_standardized_errors.openapi_serializers.ClientErrorEnum.values",
        "ServerErrorEnum": "drf_standardized_errors.openapi_serializers.ServerErrorEnum.values",
        "ErrorCode401Enum": "drf_standardized_errors.openapi_serializers.ErrorCode401Enum.values",
        "ErrorCode403Enum": "drf_standardized_errors.openapi_serializers.ErrorCode403Enum.values",
        "ErrorCode404Enum": "drf_standardized_errors.openapi_serializers.ErrorCode404Enum.values",
        "ErrorCode405Enum": "drf_standardized_errors.openapi_serializers.ErrorCode405Enum.values",
        "ErrorCode406Enum": "drf_standardized_errors.openapi_serializers.ErrorCode406Enum.values",
        "ErrorCode415Enum": "drf_standardized_errors.openapi_serializers.ErrorCode415Enum.values",
        "ErrorCode429Enum": "drf_standardized_errors.openapi_serializers.ErrorCode429Enum.values",
        "ErrorCode500Enum": "drf_standardized_errors.openapi_serializers.ErrorCode500Enum.values",
    },
    "POSTPROCESSING_HOOKS": [
        "drf_standardized_errors.openapi_hooks.postprocess_schema_enums"
    ],
    "VERSION": __api_version__,
}

DRF_STANDARDIZED_ERRORS = {
    # Per default, uncaught exceptions are not rendered to JSON in DEBUG mode, so that more information about the error can be obtained.
    # Change this flag to True, to enable JSON exceptions in DEBUG mode.
    "ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": False
}

HEALTH_CHECK = {
    # max disk usage in %, requires psutil
    "DISK_USAGE_MAX": 90,
    # minimum available memory in MB, requires psutil
    "MEMORY_MIN": 100,
}

# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailmenus.context_processors.wagtailmenus",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {"default": dj_database_url.parse(SETUP.DATABASE_URL, conn_max_age=600)}

PASSWORD_HASHERS = ["parat.core.cryptography.CustomisedArgon2PasswordHasher"]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "de"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n-l10n
USE_I18N = True
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
# Uncomment this line and add your LOCALE_PATHS if you do not want to use auto discovery
LOCALE_PATHS = [str(APPS_DIR / "locale")]

STATIC_URL = "static/"
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"

# LOGIN_URL = "/auth/login/"
# LOGOUT_URL = "/auth/logout/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

WHITENOISE_MAX_AGE = 3600

STATIC_ROOT = os.path.join(BASE_DIR, "static")

ALLOWED_HOSTS = SETUP.ALLOWED_HOSTS

AUTO_ADMIN_EMAIL = SETUP.AUTO_ADMIN_EMAIL

CSRF_TRUSTED_ORIGINS = SETUP.CSRF_HOSTS

MEDIA_URL = SETUP.MEDIA_URL
MEDIA_ROOT = SETUP.MEDIA_ROOT
MAIN_DOMAIN = SETUP.MAIN_DOMAIN

if DEBUG and SETUP.DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(8, "debug_toolbar.middleware.DebugToolbarMiddleware")

    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

if SETUP.USE_PROXY_HEADERS:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SERVER_EMAIL = SETUP.EMAIL_FROM
EMAIL_REPLYTO = SETUP.EMAIL_REPLYTO
if SETUP.EMAIL_SERVER:
    parsed = urllib.parse.urlparse(SETUP.EMAIL_SERVER)
    query = urllib.parse.parse_qs(parsed.query)
    if parsed.scheme == "console":
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    elif parsed.scheme == "smtp":
        EMAIL_HOST = parsed.hostname
        EMAIL_PORT = parsed.port
        if parsed.username:
            EMAIL_HOST_USER = urllib.parse.unquote(parsed.username)
        if parsed.password:
            EMAIL_HOST_PASSWORD = urllib.parse.unquote(parsed.password)
        EMAIL_USE_TLS = as_bool(query.get("tls"))
        EMAIL_USE_SSL = as_bool(query.get("ssl"))
    else:
        raise ValueError("Unknown schema for EMAIL_SERVER.")
NOTIFICATION_MAIL = SETUP.NOTIFICATION_MAIL

if SETUP.MEDIA_BACKEND:
    parsed = urllib.parse.urlparse(SETUP.MEDIA_BACKEND)
    query = urllib.parse.parse_qs(parsed.query)
    if parsed.scheme == "s3":
        DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
        AWS_STORAGE_BUCKET_NAME = parsed.path.lstrip("/")
        AWS_QUERYSTRING_AUTH = False
        AWS_DEFAULT_ACL = SETUP.MEDIA_BACKEND_S3_ACL
        if parsed.username is not None:
            AWS_ACCESS_KEY_ID = parsed.username
            AWS_SECRET_ACCESS_KEY = urllib.parse.unquote(parsed.password)
        if parsed.hostname is not None:
            port = parsed.port or 443
            AWS_S3_ENDPOINT_URL = f"https://{parsed.hostname}:{port}"
        if SETUP.MEDIA_URL is not None:
            media_url_parsed = urllib.parse.urlparse(SETUP.MEDIA_URL)
            AWS_S3_CUSTOM_DOMAIN = media_url_parsed.hostname
    elif parsed.scheme == "local":
        if not (MEDIA_ROOT and MEDIA_URL):
            raise ValueError(
                "You must provide MEDIA_ROOT and MEDIA_URL for a local media backend"
            )
    else:
        raise ValueError(f"Unsupported media backend {parsed.scheme}")

CACHES = {
    "default": django_cache_url.parse(SETUP.CACHES_DEFAULT or "locmem://"),
}

if SETUP.ERROR_EMAILS:
    ADMINS = [("Admin", e) for e in SETUP.ERROR_EMAILS]

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

CORS_ORIGIN_ALLOW_ALL = True  # Temporary
CORS_ORIGIN_WHITELIST = SETUP.CORS_HOSTS
CORS_ALLOW_CREDENTIALS = True
CORS_PREFLIGHT_MAX_AGE = 604800
CORS_ORIGIN_ALLOW_ALL = True  # Temporary
# wagtail
WAGTAIL_SITE_NAME = "parat"
WAGTAILADMIN_BASE_URL = SETUP.WAGTAILADMIN_BASE_URL
WAGTAILDOCS_DOCUMENT_MODEL = "core.CustomDocument"
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 50 * 1024 * 1024

# when using Wagtail, enhanced i18n is enabled by default
WAGTAIL_I18N_ENABLED = True
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("de", "German"),
    ("en", "English"),
    # only locales added here are available to wagtail
]

WAGTAILTRANSFER_COMPUTED_STAGE = (
    "staging" if SETUP.ENVIRONMENT == "production" else "production"
)

# Stage synchronization settings, example:
WAGTAILTRANSFER_SOURCES: dict = {
    f"{WAGTAILTRANSFER_COMPUTED_STAGE}": {
        "BASE_URL": f"new_customer-new_project-{WAGTAILTRANSFER_COMPUTED_STAGE}.sphericalelephant.cloud",
        "SECRET_KEY": f"{SETUP.WAGTAILTRANSFER_STAGE_KEY}",
    }
}

# This instance's secret key
WAGTAILTRANSFER_SECRET_KEY = SETUP.WAGTAILTRANSFER_SECRET_KEY

FRIENDLY_CAPTCHA_API_KEY = SETUP.FRIENDLY_CAPTCHA_API_KEY

# WAGTAILTRANSFER_UPDATE_RELATED_MODELS = []

# WAGTAILTRANSFER_LOOKUP_FIELDS = {}

# WAGTAILTRANSFER_NO_FOLLOW_MODELS = ['wagtailcore.page']

# WAGTAILTRANSFER_FOLLOWED_REVERSE_RELATIONS = [('wagtailimages.image', 'tagged_items', True)]

# WAGTAILTRANSFER_CHOOSER_API_PROXY_TIMEOUT = 5
# crispy
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# wagtailmenus
WAGTAILMENUS_FLAT_MENUS_HANDLE_CHOICES = [
    ("footer-col-products", "Produkte"),
    ("footer-col-solutions", "Lösungen"),
    ("footer-col-company", "Firma"),
    ("footer-col-services", "Services"),
    ("footer_bottom", "Bottom"),
]
WAGTAILMENUS_MAIN_MENU_ITEMS_RELATED_NAME = "menu_items"
FLAT_MENU_ITEMS_RELATED_NAME = "menu_items"
WAGTAILMENUS_MAIN_MENU_MODEL = "core.CustomMainMenu"
WAGTAILMENUS_FLAT_MENU_MODEL = "core.CustomFlatMenu"
WAGTAILMENUS_SECTION_ROOT_DEPTH = 3

# django-vite
DJANGO_VITE_ASSETS_PATH = "./ui/dist"
DJANGO_VITE_DEV_MODE = SETUP.VITE_DEV_MODE
DJANGO_VITE_DEV_SERVER_PORT = 5173
INSTALLED_APPS.append("django_vite")
STATICFILES_DIRS.append("ui/dist")
# we are not running puput as a standalone blog!
PUPUT_AS_PLUGIN = True
# puput (actually wagtail) does not play nice with user
# names containing "."
# see:
#   - https://github.com/APSL/puput/issues/198
#   - https://github.com/APSL/puput/issues/122
#   - https://github.com/wagtail/wagtail/issues/3653
PUPUT_USERNAME_FIELD = "author_name"
# PUPUT_USERNAME_REGEX = ".*"

# frontend

FRONTEND_BTN_SIZE_DEFAULT = ""
FRONTEND_BTN_SIZE_CHOICES = [
    ("btn-sm", "Small"),
    ("", "Default"),
    ("btn-lg", "Large"),
]
FRONTEND_BTN_STYLE_DEFAULT = "btn-primary"
FRONTEND_BTN_STYLE_CHOICES = [
    ("btn-primary", "Primary"),
    ("btn-secondary", "Secondary"),
    ("btn-success", "Success"),
    ("btn-danger", "Danger"),
    ("btn-info", "Info"),
    ("btn-light", "Light"),
    ("btn-dark", "Dark"),
    ("btn-outline-primary", "Outline Primary"),
    ("btn-outline-secondary", "Outline Secondary"),
    ("btn-outline-success", "Outline Success"),
    ("btn-outline-danger", "Outline Danger"),
    ("btn-outline-info", "Outline Info"),
    ("btn-outline-light", "Outline Light"),
    ("btn-outline-dark", "Outline Dark"),
]

FRONTEND_IMAGE_SHADOW_DEFAULT = ""
FRONTEND_IMAGE_SHADOW_CHOICES = [
    ("shadow-none", "None"),
    ("shadow-sm", "Small"),
    ("shadow", "Regular"),
    ("shadow-lg", "Larger"),
]

from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.DEBUG: "primary",
    message_constants.INFO: "info",
    message_constants.SUCCESS: "success",
    message_constants.WARNING: "warning",
    message_constants.ERROR: "danger",
}

# django-cookie-consent
INSTALLED_APPS.append("cookie_consent")
WAGTAILIMAGES_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp", "svg"]
MIGRATION_MODULES = {"puput": "parat.news.puput_migrations"}
