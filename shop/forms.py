from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

class AddItemForm(forms.Form):
	quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
	size = forms.CharField(required=False, widget=forms.HiddenInput)
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

	def clean_quantity(self):
		data = self.cleaned_data['quantity']
		if data > 5:
			raise ValidationError(_('Too much'))
		return data

class RemoveItemForm(forms.Form):
	item_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
	size = forms.CharField(required=False, widget=forms.HiddenInput)