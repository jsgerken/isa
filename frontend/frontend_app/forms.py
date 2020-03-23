from django import forms


class ListingForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Name:'}))
    type = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Type:'}))
    description = forms.CharField(max_length=2000, widget=forms.TextInput(
        attrs={'placeholder': 'Description:'}))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': 'Price:'}))
    warranty = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Warranty:'}))
    img_url = forms.CharField(max_length=500, label="Image URL", widget=forms.TextInput(
        attrs={'placeholder': 'Image URL:'}))
