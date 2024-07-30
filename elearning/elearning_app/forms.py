from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('type', 'first_name', 'last_name', 'email', 'photo')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('code', 'name', 'description')

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('file', )

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('description', )

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ('description', )

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('room_name', )