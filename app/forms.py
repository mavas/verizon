from django import forms

from app.validators import *


class HomeForm(forms.Form):
    url = forms.CharField(label='Youtube video URL', max_length=100, validators=[validate_youtube_video_url])
