from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import ImageUploadForm, DataUploadForm
from .encrypt import encrypt_image, decrypt_image


def encrypt(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['image']
            encrypted_img = encrypt_image(f, request.POST['password'])
            return render(request, 'download.html', {'result': encrypted_img})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


def decrypt(request):
    if request.method == 'POST':
        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            d = request.POST['data']
            decrypted_img = decrypt_image(d, request.POST['password'])
            response = HttpResponse(mimetype="image/png")
            decrypted_img.save(response, "PNG")
            return response
    else:
        form = DataUploadForm()
    return render(request, 'upload.html', {'form': form})


def success(request):
    return HttpResponse("swag!")
# Create your views here.
