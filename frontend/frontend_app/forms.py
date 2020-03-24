from django import forms

class Login(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Username:'}))
    password = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Password:'}))
    is_man = forms.BooleanField(required=False)

class CreateUser(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=14)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)


class CreateManufacturer(forms.Form):
    man_name = forms.CharField(max_length=50)
    web_url = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=14)
    password = forms.CharField(max_length=100)

#class CreateProduct(forms.Form):
    



class ListingForm(forms.Form):
    name = forms.CharField(max_length=200, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Name:'}))
    type = forms.CharField(max_length=50, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Type:'}))
    description = forms.CharField(max_length=2000, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Description:'}))
    price = forms.IntegerField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Price:'}))
    warranty = forms.CharField(max_length=50, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Warranty:'}))
    img_url = forms.CharField(max_length=500, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Image URL:'}))
