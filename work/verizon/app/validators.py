import re

from django.core.exceptions import ValidationError


def validate_video_url(u):
    idts = ['ghY9xrSJexk', 'QJHcWIXymHA']

    for idt in idts:
        s = r'^https://www.youtube.com/watch?v=%s$' % idt
        m = re.match(s, u)
        if m:
            return

    raise ValidationError("Not a valid video URL.")
