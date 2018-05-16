from django.db import IntegrityError
from django.shortcuts import render, Http404, redirect, get_object_or_404, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import *
from hospital_queue_app.models import Patient, Heap, Procedure
from .models import Receptionist
from .forms import PatientForm

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ReceptionistSerializer

from django.utils import timezone


# api для реєстраторів
class ReceptionistAPI(APIView):
    def get(self, request, pk):
        departments_v = Receptionist.objects.get(pk=pk)
        serializer = ReceptionistSerializer(departments_v, many=False)
        return Response(serializer.data)

    def post(self, request, pk):
        departments_v = Receptionist.objects.get(pk=pk)
        serializer = ReceptionistSerializer(departments_v, many=False)
        return Response(serializer.data)


# Авторизація
def log_in(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = get_object_or_404(Receptionist, username=username, password=password)
        # user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('hospital_reception_app:home')
        else:
            raise Http404
    except Http404:
        return render(request, 'hospital_reception_app/login.html', {"message": "Неправильний логін або пароль"})
    except MultiValueDictKeyError:
        return render(request, 'hospital_reception_app/login.html')


# Не Авторизація
def log_out(request):
    logout(request)
    return redirect('hospital_reception_app:login')


# Виведення основної сторінки для реєстратора
def index_of_receptionist(request):
    return render(request, 'hospital_reception_app/index.html')


# Функція пошуку пацієнтів
def search_patient(request):
    try:
        surname = request.POST['surname']
        name = request.POST['name']
        return render(request, 'hospital_reception_app/patients_result.html',
                      {
                          'patients': Patient.objects.filter(surname=surname, name=name)
                      })
    except MultiValueDictKeyError:
        return HttpResponse("<table></table>Не вдалося знайти жодного пацієнта<script></script>")


# Функція що виводить форму для додавання пацієнта
def create_patient_request(request):
    return render(request, "hospital_reception_app/patients_registration.html",
                  {
                      'form': PatientForm()
                  })


# Функція додавання пацієнта
def create_patient_response(request):
    if request.POST:
        patient = Patient.objects.create(
            surname=request.POST['surname'],
            name=request.POST['name'],
            father_name=request.POST['father_name'],
            date_of_birth=request.POST['date_of_birth'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            patient_status=request.POST['patient_status']
        )
        patient.save()
    return redirect('hospital_reception_app:home')


# Функція зміни статусу присутності пацієнта
def change_patient_present_status(request):
    try:
        if request.POST:
            patient = Patient.objects.get(pk=int(request.POST["patient_pk"]))
            if request.POST["value"] == "true":
                patient.patient_present_state = 3
                patient.patient_present_time = timezone.localtime(timezone.now())
                patient.save()
                return HttpResponse("Статус пацієнта " + str(patient) + " змінено на присутній")
            else:
                patient.patient_present_state = 1
                patient.save()
                return HttpResponse("Статус пацієнта " + str(patient) + " змінено на відсутній")

    except MultiValueDictKeyError:
        return HttpResponse("При спробі змінення статусу пацієнта виникла помилка")


# Додавання пацієнта в чергу
def assign_procedure_to_patient(request, pk=None):
    if pk is not None:
        try:
            patient_id = pk
            return render(
                request,
                'hospital_reception_app/assign_procedure.html',
                {
                    "patient": Patient.objects.get(pk=patient_id),
                    "procedures": Procedure.objects.all().filter(available_to_registrars=True)
                }
            )
        except MultiValueDictKeyError:
            return HttpResponse("При виведенні сторінки виникла помилка")
    else:
        try:
            patient_id = request.POST["patient_id"]
            procedure_id = request.POST["procedure_id"]
            record = Heap.objects.create(patient_id=patient_id, procedure_id=procedure_id)
            record.save()
            return HttpResponse("Пацієнт " + str(Patient.objects.get(pk=patient_id)) +
                                " був доданий в чергу " + str(Procedure.objects.get(pk=procedure_id)))
        except IntegrityError:
            return HttpResponse("Пацієнт " + str(Patient.objects.get(pk=request.POST["patient_id"])) +
                                " вже був доданий в чергу")
        except MultiValueDictKeyError:
            return HttpResponse(
                "При додаванні пацієнта в чергу виникла помилка! "
                "<a href ='{% url \'hospital_reception_app:assign_procedure_to_patient\' "
                "pk=" + request.POST["patient_id"] + "%}'>Спробуйте ще раз</a>"
            )


def procedures_menu_list(request):
    return render(request, "hospital_reception_app/procedures_menu.html", {"procedures": Procedure.objects.all()})


def procedures_detail_queue(request, procedure_id=None):
    return render(request, "hospital_reception_app/procedure_detail_queue.html",
                  {"set": Heap.objects.all().filter(procedure=procedure_id)})
