from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(required = False)
    min_price = forms.IntegerField(required = False, label = 'Minimum price')
    max_price = forms.IntegerField(required = False, label = 'Maximum price')