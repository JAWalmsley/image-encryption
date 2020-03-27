from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File
from django.http import HttpResponseRedirect
from .forms import ImageUploadForm, DataUploadForm
from .encrypt import encrypt_image, decrypt_image


def encrypt(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['image']
            encrypted_img = encrypt_image(f, request.POST['password'])
            return render(request, 'download.html', {'result': encrypted_img.decode()})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form, 'next_step_url': '/decrypt', 'next_step': 'Decrypt'})


def decrypt(request):
    if request.method == 'POST':
        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            d = request.POST['data']
            decrypted_img = decrypt_image(d.encode(), request.POST['password'])
            return render(request, 'download.html', {'result': decrypted_img})
    else:
        form = DataUploadForm()
    return render(request, 'upload.html', {'form': form, 'next_step_url': '/encrypt', 'next_step': 'Encrypt'})


def success(request):
    return HttpResponse("swag!")
# Create your views here.
