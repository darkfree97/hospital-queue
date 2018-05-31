from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Робочий кабінет лікаря<br>Буде достуний в новішій версії програми<br>Вибачте за незручності :(")
