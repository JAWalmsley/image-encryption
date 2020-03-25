from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import ImageUploadForm
from .encrypt import encrypt_data, create_signature


def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['image']
            print("Encryption result", encrypt_data(f, request.POST['password']))
            return HttpResponseRedirect('/upload/success')
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


def success(request):
    return HttpResponse("swag!")
# Create your views here.
