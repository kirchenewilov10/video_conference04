from django.utils.translation import gettext, gettext_lazy as _

from django import forms
from django.forms import ModelForm

from frontend.dashboard.models import useravatar

class ImageForm(ModelForm):
    class Meta:
        model = useravatar
        exclude = ['id']