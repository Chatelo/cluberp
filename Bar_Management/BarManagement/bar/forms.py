from django import forms
from .models import Drink



class OrderForm(forms.Form):
    drink = forms.ModelChoiceField(queryset=Drink.objects.all())
    quantity = forms.IntegerField(min_value=1)

class SupplierForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ['name', 'price', 'description', 'stock_level']
