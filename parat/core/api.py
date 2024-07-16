from logging import getLogger

import requests
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from parat import __api_version__, __version__
from parat.core.serializers import VersionSerializer

logger = getLogger(__name__)


@extend_schema(
    responses=VersionSerializer,
    description=_("core.documentation.openapi_get_version_description"),
    summary=_("core.documentation.openapi_get_version_summary"),
)
@api_view(["GET"])
def get_version(request):
    return Response({"version": __version__, "api_version": __api_version__})


@api_view(["GET"])
def get_font(request):
    try:
        url = "https://fast.fonts.net/lt/1.css?apiType=css&c=b8cea8d9-7bfe-42e4-afcd-67b32d3df06b&fontids=1473687,1473690,1473693,1473696,1473699,1473702,1473704,1473706,1473708,1473710,1473712,1473714,1473716,1473718,1473720,1473722,1473724,1473726,1473728,1473730,1473732,1473734,1473737,1473740,1473744,1473748,1473750,1473752"
        response = requests.get(url)
        logger.info(f"font response {response}")
    except Exception as e:
        logger.info("error tracking font!", exc_info=e)

    return Response(status=status.HTTP_204_NO_CONTENT)
