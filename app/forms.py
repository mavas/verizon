from django import forms


class HomeForm(forms.Form):
    url = forms.CharField(label='Youtube video URL', max_length=100)
