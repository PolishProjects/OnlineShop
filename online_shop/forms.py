from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



class ProfileUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-fn'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-ln'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'id': 'checkout-email'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-company'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-country'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-city'}))
    postal_code = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-zip'}))
    address1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-address1'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-address2'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number',]
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'checkout-phone'}),
        }


    def clean_email(self):
        email = self.cleaned_data['email']
        if email and validate_email(email):
            raise ValidationError("Enter a valid email address.")
        elif User.objects.filter(email=email).exists():
            raise ValidationError("E-mail: {} already exist!".format(email))
        return email