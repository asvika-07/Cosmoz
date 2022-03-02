from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from Accounts.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = (
            "FirstName",
            "LastName",
            "RegistrationID",
            "email",
            "MobileNumber",
            "DateOfBirth",
            "UserType",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            account = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f"{account} already exist")


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class UserUpdateForm(forms.ModelForm):

    ProfilePicture = forms.ImageField()
    Description = forms.CharField()

    widget = (
        {
            "Description": forms.Textarea(attrs={"rows": 6, "cols": 15}),
        },
    )

    class Meta:
        model = User
        fields = ("ProfilePicture", "Description")

    def save(self, commit=True):
        account = super(UserUpdateForm, self).save(commit=False)
        # account.email = self.cleaned_data['email'].lower()
        account.ProfilePicture = self.cleaned_data.get("ProfilePicture", None)
        account.Description = self.cleaned_data["Description"]
        # account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account

    Description.widget.attrs["class"] = "text_area form-control"
    # ProfilePicture.widget.attrs['class']='form-control-file'
    # ProfilePicture.label_classes=("button",)