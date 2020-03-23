from django import forms

class Login(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    is_man = forms.BooleanField(required=False)

class CreateUser(forms.Form):
    man_name = forms.CharField(max_length=50)
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
    
