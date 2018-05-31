from django.contrib.auth import login, logout
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError

from hospital_queue_app.models import Patient


def index(request):
    return render(request, 'hospital_patient_app/index.html')


# Авторизація
def log_in(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
        user = get_object_or_404(Patient, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('hospital_patient_app:home')
        else:
            raise Http404
    except Http404:
        return render(request, 'hospital_patient_app/authorization.html', {"message": "Неправильний логін або пароль"})
    except MultiValueDictKeyError:
        return render(request, 'hospital_patient_app/authorization.html')


# Не Авторизація
def log_out(request):
    logout(request)
    return redirect('hospital_patient_app:login')


