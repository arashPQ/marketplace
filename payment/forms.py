from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full-name'}), required=True)

    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email'}), required=True)
	
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Address 1'}), required=True)
	
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}), required=False)
	
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'City'}), required=True)
	
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'State'}), required=False)
	
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Country'}), required=True)

    shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Zip-code'}), required=False)					#		postal code

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_country', 'shipping_zipcode']

        exclude = ['user']

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on card'}), required=True)
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'card number'}), required=True)
    card_exp_date = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'card Expration date'}), required=True)
    card_cvv = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'card CVV2 code'}), required=True)
    card_address = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing address'}), required=True)
    card_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing city'}), required=True)
    card_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing state'}), required=True)
    card_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing country'}), required=True)
    card_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing ZipCode'}), required=True)