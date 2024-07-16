from rest_framework.serializers import Serializer, RegexField

# See: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
semver_regex = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"


class VersionSerializer(Serializer):
    version = RegexField(semver_regex)
    api_version = RegexField(semver_regex)
