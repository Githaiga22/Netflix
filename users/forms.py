from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only." 
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        help_text="Enter a valid email address."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
          help_text=mark_safe(  #Ensures the list is rendered properly
            "<ul>"
            "<li><span>Your password can’t be too similar to your other personal information.</span></li>"
            "<li><span>Your password must contain at least 8 characters.</span></li>"
            "<li><span>Your password can’t be a commonly used password.</span></li>"
            "<li><span>Your password can’t be entirely numeric.</span></li>"
            "</ul>"
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        help_text="Enter the same password as before, for verification."
    )

    birth = forms.DateField(
        widget=forms.DateInput(attrs = {'type': 'date'}),
        required=True,
        help_text="Enter date of birth"
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'birth']
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email
    def clean_birth(self):
        birth = self.cleaned_data.get('birth')
        if birth and birth > date(2008, 12, 31):
            raise forms.ValidationError("Birth date cannot be later than 2008.")
        return birth
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True  
        user.save()
       
        customer = Customer.objects.create(
            user=user,
            birth = self.cleaned_data['birth'],
        )
        customer.save()
        
        return user



class CompanySignUpForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only." 
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        help_text="Enter a valid email address."
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
          help_text=mark_safe(  # Ensures the list is rendered properly
            "<ul>"
            "<li><span>Your password can’t be too similar to your other personal information.</span></li>"
            "<li><span>Your password must contain at least 8 characters.</span></li>"
            "<li><span>Your password can’t be a commonly used password.</span></li>"
            "<li><span>Your password can’t be entirely numeric.</span></li>"
            "</ul>"
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        help_text="Enter the same password as before, for verification."
    )
    field = forms.ChoiceField(
        choices=Company._meta.get_field('field').choices,  #  Dynamically get choices
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'field']
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True  
        if commit:
            user.save()
            company = Company.objects.create(
                user=user,
                field=self.cleaned_data['field'],
            )
            company.save()
        return user


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
