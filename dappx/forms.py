from django import forms
from .models import Appointment # , UserProfileInfo
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


# class UserProfileInfoForm(forms.ModelForm):
#     class Meta:
#         model = UserProfileInfo
#         fields = ('portfolio_site', 'profile_pic')


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "date",
            "time_start",
            "time_end",
            "appointment_with"
        ]
