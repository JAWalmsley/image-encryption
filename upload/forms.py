from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    password = forms.CharField(widget=forms.PasswordInput, max_length=50)


class DataUploadForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, max_length=50)
    data = forms.FileField()
