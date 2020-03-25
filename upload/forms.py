from django import forms


class ImageUploadForm(forms.Form):
    password = forms.CharField(max_length=50)
    image = forms.ImageField()
