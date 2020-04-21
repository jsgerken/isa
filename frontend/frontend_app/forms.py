from django import forms


class CreateListing(forms.Form):
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


class Login(forms.Form):
    username = forms.CharField(max_length=50, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Username:'}))
    password = forms.CharField(max_length=50, label="", widget=forms.PasswordInput(
        attrs={'placeholder': 'Password:'}))
    is_man = forms.BooleanField(
        required=False, label="I am logging in as a manufacturer")


class CreateUser(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    email = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=14)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)


class CreateManufacturer(forms.Form):
    man_name = forms.CharField(max_length=50, label="Company Name")
    email = forms.CharField(max_length=100)
    web_url = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=14)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class Profile(forms.Form):
    username = forms.CharField(max_length=50, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Username:'}))
    email = forms.CharField(max_length=100, label="", widget=forms.TextInput(
        attrs={'placeholder': 'E-Mail:'}))
    phone_number = forms.CharField(max_length=14, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number:'}))
    first_name = forms.CharField(max_length=30, label="", widget=forms.TextInput(
        attrs={'placeholder': 'First Name:'}))
    last_name = forms.CharField(max_length=30, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Last Name:'}))


class ForgotPassword(forms.Form):
    reset_info = forms.CharField(max_length=100, label="Email/Username")
    is_man = forms.BooleanField(required=False, label="I am a manufactuer")


class ResetPassword(forms.Form):
    new_password = forms.CharField(
        max_length=32, widget=forms.PasswordInput(), label="New password")
    confirm_password = forms.CharField(
        max_length=32, widget=forms.PasswordInput(), label="Confirm password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "New password and confirm password do not match"
            )
