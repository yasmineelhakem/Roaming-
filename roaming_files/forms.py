from django import forms
from .models import RoamingIn, RoamingOut

class RoamingInForm(forms.ModelForm):
    class Meta:
        model = RoamingIn
        fields = ['input_file']

class RoamingOutForm(forms.ModelForm):
    class Meta:
        model = RoamingOut
        fields = ['input_file']
