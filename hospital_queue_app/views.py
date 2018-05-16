from django.shortcuts import render
from .models import Patient, Doctor, Heap
from django.utils import timezone


def index(request):
    return render(request, 'hospital_queue_app/index.html', {'patients': Patient.objects.all()})


def get_doctors(request):
    return render(request, "hospital_queue_app/doctors.html", {'doctors': Doctor.objects.all()})


def universal_queue(request):
    heap = Heap.objects.all().order_by("-patient__patient_status", "patient__patient_present_time")\
        .exclude(patient__patient_present_state=1).filter(patient__patient_present_time__day=timezone.now().today().day)
    procedures = set()
    for item in heap:
        procedures.add(item.procedure.name)
    return render(request, "hospital_queue_app/universal_queue.html", {'procedures': procedures, 'queues_heap': heap})

