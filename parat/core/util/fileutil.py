import os
import secrets

from django.utils import timezone


def upload_generic_namer(prefix, instance, filename):
    """
    Names uploaded images.

    By default, obscures the original name with a random urlsafe ID.
    """
    _, old_extension = os.path.splitext(filename)
    new_filename = secrets.token_urlsafe(20)
    now = timezone.now()
    return os.path.join(
        prefix,
        str(now.year),
        str(now.month),
        str(now.day),
        f"{new_filename}{old_extension}",
    )
