from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class PhotoUploadForms(forms.Form):
    photo = forms.ImageField()
class RegistrationForm(forms.Form):
    username = forms.CharField(label="Title of the publication", required=True)
    password = forms.CharField(label="Publication", widget=forms.Textarea(attrs={'rows':10}))

