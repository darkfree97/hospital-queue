from django import forms
from hospital_queue_app.models import Patient
import datetime


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'surname',
            'name',
            'father_name',
            'date_of_birth',
            'phone',
            'email',
            'patient_status'
        ]
