from django import forms
from .models import CoffeeOrder, CoffeeVariety, Store

class CoffeeVarietyForm(forms.Form):
    coffee_variety = forms.ModelChoiceField(
        queryset=CoffeeVariety.objects.all(),
        label="Choose a coffee variety",
        empty_label="Select a coffee",
        widget=forms.Select(attrs={
            "class": "mt-2 block w-full rounded-xl border border-stone-300 bg-white px-4 py-3 text-stone-900 shadow-sm outline-none transition focus:border-amber-600 focus:ring-4 focus:ring-amber-100"
        }),
    )


class CoffeeOrderForm(forms.ModelForm):
    class Meta:
        model = CoffeeOrder
        fields = ('coffee_variety', 'store', 'quantity')
        widgets = {
            'coffee_variety': forms.Select(attrs={'class': 'mt-2 block w-full rounded-xl border border-stone-300 bg-white px-4 py-3 text-stone-900 shadow-sm outline-none transition focus:border-amber-600 focus:ring-4 focus:ring-amber-100'}),
            'store': forms.Select(attrs={'class': 'mt-2 block w-full rounded-xl border border-stone-300 bg-white px-4 py-3 text-stone-900 shadow-sm outline-none transition focus:border-amber-600 focus:ring-4 focus:ring-amber-100'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 20, 'class': 'mt-2 block w-full rounded-xl border border-stone-300 bg-white px-4 py-3 text-stone-900 shadow-sm outline-none transition focus:border-amber-600 focus:ring-4 focus:ring-amber-100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coffee_variety'].queryset = CoffeeVariety.objects.all()
        self.fields['store'].queryset = Store.objects.all()
        self.fields['coffee_variety'].empty_label = 'Select a coffee'
        self.fields['store'].empty_label = 'Select a store'

    def clean(self):
        cleaned_data = super().clean()
        coffee_variety = cleaned_data.get('coffee_variety')
        store = cleaned_data.get('store')
        if coffee_variety and store and not store.coffee_varieties.filter(pk=coffee_variety.pk).exists():
            raise forms.ValidationError(f'{store.name} does not currently serve {coffee_variety.name}. Please choose another store or coffee.')
        return cleaned_data
