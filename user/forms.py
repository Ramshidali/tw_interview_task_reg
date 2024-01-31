import re
from django import forms
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,EmailInput

from user.models import UserDetails


class userDetailsForm(forms.ModelForm):

    class Meta:
        model = UserDetails
        fields = ['name','mobile','email','role','country','nationality','password']

        widgets = {
            'name': TextInput(attrs={'class':'form-control'}),
            'mobile': TextInput(attrs={'class':'form-control'}),
            'email': EmailInput(attrs={'class':'form-control'}),
            'role': Select(attrs={'class':'form-control'}),
            'country': TextInput(attrs={'class':'form-control'}),
            'nationality': TextInput(attrs={'class':'form-control'}),
            'password': TextInput(attrs={'class':'form-control'}),
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    def clean_username(self):
        username = self.cleaned_data['username']

        if not username:
            raise forms.ValidationError("Please enter a username.")

        if '@' in username:
            # Check if the username is a valid email format
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', username):
                raise forms.ValidationError("Invalid email format.")

        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        if not password:
            raise forms.ValidationError("Please enter a valid password.")

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        return password


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Re-enter Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')


        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        if password and len(password) < 8:
            raise forms.ValidationError("Please enter a minimum of 8 characters")

        if password and len(password) > 20:
            raise forms.ValidationError("Please enter a maximum of 20 characters for the password")

        return cleaned_data