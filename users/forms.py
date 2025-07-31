from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # Validate if email already exists
    if User.objects.filter(email=value).exists():
        raise ValidationError(f"{value} is already taken.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    birth_date = forms.DateField(widget=DateInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'birth_date')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
            customer = Customer.objects.create(user=user)
            customer.birth_date = self.cleaned_data.get('birth_date')
            customer.save()
        return user


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    field = forms.ChoiceField(choices=Company._meta.get_field('field').choices)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'field')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        if commit:
            user.save()
            company = Company.objects.create(user=user)
            company.field = self.cleaned_data.get('field')
            company.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Email',
        'autocomplete': 'off'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

class RequestServiceForm(forms.Form):
 request_description = forms.CharField(
 widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your request description'})
 )