from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from customer.models import Profile

class HomeForm(forms.Form):
    email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={'placeholder': 'name@example.com'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write your message here'}))
    check = forms.BooleanField(required=False)

class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dob','blood_grp','gender','mobile')     