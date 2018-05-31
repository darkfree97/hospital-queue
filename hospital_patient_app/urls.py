from django.conf.urls import url
from hospital_patient_app import views


app_name = "hospital_patient_app"

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^login/', views.log_in, name="login"),
    url(r'^logout/', views.log_out, name="logout"),
]