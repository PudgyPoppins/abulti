from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Order

from django_countries import countries
COUNTRY_CODE_LIST = dict(countries).keys()

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

class AddItemForm(forms.Form):
	quantity = forms.TypedChoiceField(
		choices=PRODUCT_QUANTITY_CHOICES, 
		coerce=int, 
		widget=forms.Select(attrs={'class': 'addItem'}),
	)
	size = forms.CharField(required=False, widget=forms.HiddenInput)
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

	def clean_quantity(self):
		data = self.cleaned_data['quantity']
		if data > 5:
			raise ValidationError(_('Too many items ordered at once!'))
		return data

class RemoveItemForm(forms.Form):
	item_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
	size = forms.CharField(required=False, widget=forms.HiddenInput)



class CheckoutForm(forms.Form):
	name = forms.CharField()
	email = forms.EmailField()

	shipping_address = forms.CharField(
		label = 'Address',
		min_length = 5,
		widget=forms.TextInput(attrs={'placeholder': '1234 Main Street'})
	)
	shipping_address2 = forms.CharField(
		label = 'Address 2 (optional)',
		required=False,
		widget=forms.TextInput(attrs={'placeholder': 'Apt num, Suite (optional)'})
	)
	shipping_city = forms.CharField(label = 'City', min_length = 3)
	shipping_state = forms.CharField(label = 'State / Province', min_length = 2)
	shipping_country = CountryField(blank_label='Select a Country').formfield(
		label = 'Country',
		widget=CountrySelectWidget(
			layout = '{widget}',
		)
	)
	shipping_zip = forms.CharField(label = 'Zip / Postal Code', min_length = 2)

	billing_address = forms.CharField(
		required = False,
		label = 'Address',
		widget=forms.TextInput(attrs={'placeholder': '1234 Main Street'})
	)
	billing_address2 = forms.CharField(
		required = False,
		label = 'Address 2 (optional)',
		widget=forms.TextInput(attrs={'placeholder': 'Apt num, Suite (optional)'})
	)
	billing_city = forms.CharField(required = False, label = 'City')
	billing_state = forms.CharField(required = False, label = 'State / Province')
	billing_country = CountryField(blank_label='Select a Country').formfield(
		required = False,
		label = 'Country',
		widget=CountrySelectWidget(
			layout = '{widget}',
		)
	)
	billing_zip = forms.CharField(required = False, label = 'Zip / Postal Code',)

	same_billing_address = forms.BooleanField(required=False, label='Billing address is the same as my shipping address', initial=True)

	notes = forms.CharField(label = 'Notes or Instruction (optional)', required=False)

	paid = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

	'''
	def clean(self):
		if self.cleaned_data['same_billing_address']:
			if self.cleaned_data['billing_address'] != self.cleaned_data['shipping_address'] or self.cleaned_data['billing_address2'] != self.cleaned_data['shipping_address2']:
				raise ValidationError(_("Addresses should match, but they don't."))
			if self.cleaned_data['billing_zip'] != self.cleaned_data['shipping_zip']:
				raise ValidationError(_("Zip codes should match, but they don't."))
			if self.cleaned_data['billing_city'] != self.cleaned_data['shipping_city']:
				raise ValidationError(_("Cities should match, but they don't."))
			if self.cleaned_data['billing_state'] != self.cleaned_data['shipping_state']:
				raise ValidationError(_("State / Provinces should match, but they don't."))
			if self.cleaned_data['billing_country'] != self.cleaned_data['shipping_country']:
				raise ValidationError(_("Countries should match, but they don't."))
	'''
	def clean(self):
		if self.cleaned_data['same_billing_address'] != True and (self.cleaned_data['billing_address'] == '' or self.cleaned_data['billing_address2'] == '' or self.cleaned_data['billing_city'] == '' or self.cleaned_data['billing_state'] == '' or self.cleaned_data['billing_zip'] == '' or self.cleaned_data['billing_country'] == ''):
			raise ValidationError(_("You must provide all billing information"))

	def clean_shipping_country(self):
		shipping_country = self.cleaned_data['shipping_country']
		if shipping_country not in COUNTRY_CODE_LIST:
			raise ValidationError(_('Please select a valid country'))
		return shipping_country

	def clean_billing_country(self):
		billing_country = self.cleaned_data['billing_country']
		if billing_country not in COUNTRY_CODE_LIST:
			raise ValidationError(_('Please select a valid country'))
		return billing_country

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')  
		super(CheckoutForm, self).__init__(*args, **kwargs)