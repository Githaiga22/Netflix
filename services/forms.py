from django import forms

from .models import Service, RequestService

from django.core.validators import MinValueValidator



class CreateNewService(forms.ModelForm):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)
    class Meta:
        model = Service
        fields = ['name', 'description', 'price_hour', 'field']

    def __init__(self, *args, choices=None, **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)

        # Add choices to the 'field' field
        if choices:
            self.fields['field'].choices = choices

        # Adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'



class RequestServiceForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
    )
    hours = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'service time (in hours)'}),
        validators=[MinValueValidator(0)]
    )
    class Meta:
        model = RequestService
        fields = ['address', 'hours']
    
