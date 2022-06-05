import re

from django.core.exceptions import ValidationError


def validate_youtube_video_url(u):
    m = re.match('^https://www.youtube.com/watch?v=ghY9xrSJexk$', u)
    if not m:
        raise ValidationError("Not a youtube video URL.")
