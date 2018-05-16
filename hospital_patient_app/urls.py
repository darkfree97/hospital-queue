from django.conf.urls import url
from hospital_patient_app import views


app_name = "hospital_patient_app"

urlpatterns = [
    url(r'^index/', views.index, name="index"),
]