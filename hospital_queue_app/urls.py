from django.conf.urls import url
from hospital_queue_app import views


app_name = "hospital_queue_app"

urlpatterns = [
    url(r'^index/', views.index, name="index"),
    url(r'^doctors/', views.get_doctors, name="doctors"),
    url(r'^', views.universal_queue, name="all"),
]
