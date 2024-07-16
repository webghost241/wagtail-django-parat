import os
from collections import namedtuple
from urllib.parse import parse_qs, urlencode, urlparse, urlsplit, urlunparse

from django import template

register = template.Library()

# {% if self.auto_play %}?autoplay=1{% endif %}&mute=1&rel=0

Components = namedtuple(
    typename="Components",
    field_names=["scheme", "netloc", "url", "path", "query", "fragment"],
)


@register.simple_tag(name="video_url")
def video_url(video_url: str, **kwargs):
    url = urlparse(video_url)
    video_id = None
    if url.hostname == "www.youtube.com" or url.hostname == "youtube.com":
        video_id = parse_qs(url.query).get("v", [None])[0]
    elif (
        url.hostname == "youtube-nocookie.com"
        or url.hostname == "www.youtube-nocookie.com"
    ):
        video_id = os.path.split(url.path)[1]
    else:
        # TODO: vimeo
        return video_url

    if not video_id:
        raise RuntimeError("invalid yt url")

    query_parameters = {
        "autoplay": "1" if kwargs.get("autoplay", True) else "0",
        "mute": "1" if kwargs.get("mute", True) else "0",
        "rel": "1" if kwargs.get("rel", False) else "0",
    }

    return urlunparse(
        Components(
            scheme="https",
            netloc="www.youtube-nocookie.com",
            query=urlencode(query_parameters),
            url=f"/embed/{video_id}",
            path="",
            fragment="",
        )
    )


@register.filter(name="url_to_fqdn")
def url_to_fqdn(url):
    return "{0.netloc}".format(urlsplit(url))
