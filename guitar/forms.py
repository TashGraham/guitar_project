from django import forms
from django.contrib.auth.models import User
from guitar.models import UserProfile, Category, Part

class PartForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the name of the part.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    sustain = forms.FloatField(initial=-1.0, #if value is -1 that means it is not relevant info
                               max_value=5,
                               min_value=0,
                               help_text="Sustain: ")
    warmth = forms.FloatField(initial=-1.0,
                               max_value=5,
                               min_value=0,
                               help_text="Warmth: ")
    weight = forms.FloatField(initial=-1.0,
                               max_value=5,
                               min_value=0,
                               help_text="Weight: ")
    pic = forms.ImageField(help_text="Please enter a picture here", required=False)

    class Meta:
        model = Part
        fields = ('name', 'sustain', 'warmth', 'weight', )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', )
