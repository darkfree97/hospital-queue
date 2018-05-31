from django.shortcuts import render


def menu_index(request):
    return render(request, "menu/index.html")
