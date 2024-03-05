from django import forms

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='from_date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='until_date', widget=forms.DateInput(attrs={'type': 'date'}))

class DeliveryTypesForm(forms.Form):
    filter_option1 = forms.BooleanField(required=False)