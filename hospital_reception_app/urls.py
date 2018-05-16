from django.conf.urls import url
from . import views

app_name = "hospital_reception_app"

urlpatterns = [
    url(r'^login/', views.log_in, name="login"),
    url(r'^logout/', views.log_out, name="logout"),
    url(r'^$', views.index_of_receptionist, name="home"),
    url(r'^search_result/', views.search_patient, name="search_patient"),
    url(r'^patient/signup/$', views.create_patient_request, name="create_patient_request"),
    url(r'^patient/signup/confirm', views.create_patient_response, name="create_patient_response"),
    url(r'^patient/present/toggle', views.change_patient_present_status, name="patient_present_toggle"),
    url(r'^patient/assign/procedure', views.assign_procedure_to_patient, name="assign_procedure_to_patient"),
    url(r'^patient/(?P<pk>\d+)/assign/procedure', views.assign_procedure_to_patient,
        name="assign_procedure_to_patient_with_id"),
    url(r'procedures/$', views.procedures_menu_list, name="procedures"),
    url(r'procedures/detail=(?P<procedure_id>\d+)', views.procedures_detail_queue, name="procedures_detail"),
    url(r'^api/receptionist/(?P<pk>\d+)', views.ReceptionistAPI.as_view()),
]
