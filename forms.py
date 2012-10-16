from django import forms
from cart import Cart

class CartForm(forms.ModelForm):
    """A form for the Cart model."""

    is_eu_cart = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit(); return false'}))

    class Meta:
        model = Cart
        fields = ('is_eu_cart',)
