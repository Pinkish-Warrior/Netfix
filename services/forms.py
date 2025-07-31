from django import forms
from users.models import Company  # Assuming Company is used elsewhere

class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00
    )
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices=None, **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)

        # Set choices for the 'field' dropdown
        if choices:
            self.fields['field'].choices = choices

        # Add placeholders
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter Service Name',
            'autocomplete': 'off'
        })
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'


class RequestServiceForm(forms.Form):
    request_description = forms.CharField(
    widget=forms.Textarea(attrs={'placeholder': 'Enter your request description'})
    )

    def __init__(self, *args, **kwargs):
        super(RequestServiceForm, self).__init__(*args, **kwargs)

        # Add placeholder
        self.fields['request_description'].widget.attrs['placeholder'] = 'Enter your request description'
