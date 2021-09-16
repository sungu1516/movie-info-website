from django import forms
from django.forms import fields
from .models import Movies


class MoviesForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = '__all__'