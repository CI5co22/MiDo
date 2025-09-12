from django.shortcuts import render, redirect, get_object_or_404
# from .models import Tareas
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, "home.html")

def AgregarReceta(request):
    return render(request, "agregarReceta.html")

def RecetaDetalle(request, id):
    return render(request, "recetaDetalle.html")