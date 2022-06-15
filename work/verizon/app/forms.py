from django import forms

from app.validators import validate_video_url


class HomeForm(forms.Form):
    url = forms.CharField(label='Video URL', max_length=100, validators=[validate_video_url])
