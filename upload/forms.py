from django import forms


class ImageUploadForm(forms.Form):
    password = forms.CharField(max_length=50)
    image = forms.ImageField()


class DataUploadForm(forms.Form):
    password = forms.CharField(max_length=50)
    data = forms.CharField()
