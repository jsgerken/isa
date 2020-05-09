from django import forms


class CreateListing(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Intel Core i5-9600K'}))
    # type = forms.CharField(max_length=50, widget=forms.TextInput(
    #     attrs={'placeholder': 'CPU'}))
    type= forms.CharField(label='Type', widget=forms.Select(choices=[
        ("CPU","CPU"),
        ("GPU","GPU"),
        ("Motherboard","Motherboard"),
        ("Cases","Cases"),
        ("Fans","Fans"),
        ("PSU","Power Supply Unit"),
        ("Monitor","Monitor"),
        ("MnK","Mice and Keyboards"),
        ("Cables","Cables"),
    ]))
    description = forms.CharField(max_length=2000, widget=forms.TextInput(
        attrs={'placeholder': '9th Gen Intel Processor|Intel UHD Graphics 630'}))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': '300'}))
    warranty = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'placeholder': '60 days'}))
    # img_url = forms.CharField(max_length=500, label="Image URL", widget=forms.TextInput(
    #     attrs={'placeholder': 'REMEMBER TO REMOVE'}))
    product_img = forms.ImageField(label="Product Image")

    def clean(self):
        cleaned_data = super().clean()
        get_image = cleaned_data.get('product_img')
        # if the size of the image is greater than ~7 MB , throw error
        if get_image.size > 7000000:
            self.add_error('product_img', forms.ValidationError(
                "Product Image must be less than 7.0 MB. Your image: " +
                str(round(get_image.size/(1000000), 1)) + " MB"
            ))


class Login(forms.Form):
    username = forms.CharField(max_length=50, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=50, label="", widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    is_man = forms.BooleanField(
        required=False, label="I am logging in as a manufacturer")


class CreateUser(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    email = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=14)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('password', forms.ValidationError(
                "Password and confirm password do not match"))
            self.add_error('confirm_password',forms.ValidationError(""))


class CreateManufacturer(forms.Form):
    man_name = forms.CharField(max_length=50, label="Company Name")
    email = forms.CharField(max_length=100)
    web_url = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=14)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('password', forms.ValidationError(
                "Password and confirm password do not match"))
            self.add_error('confirm_password',forms.ValidationError(""))


class Profile(forms.Form):
    username = forms.CharField(max_length=50, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    email = forms.CharField(max_length=100, label="", widget=forms.TextInput(
        attrs={'placeholder': 'E-Mail'}))
    phone_number = forms.CharField(max_length=14, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number'}))
    first_name = forms.CharField(max_length=30, label="", widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}))


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
