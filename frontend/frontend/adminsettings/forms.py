from django.utils.translation import gettext, gettext_lazy as _

from django import forms
from django.forms import ModelForm

from frontend.adminsettings.models import software

class SoftwareForm(ModelForm):
    class Meta:
        model = software
        exclude = ['id']