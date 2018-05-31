from django.conf.urls import url

from hospital_doctor_app import views

app_name = "hospital_doctor_app"


urlpatterns = [
    url(r'', views.index)
]