from django.shortcuts import render, redirect, get_object_or_404
# from .models import Tareas
from django.http import JsonResponse
from .models import Receta, Medicamento
import json


# Create your views here.
def index(request):
    
    if request.method == 'POST':
        Receta.objects.create(
            doc = request.POST.get('doc'),
            fecha = request.POST.get('fecha'),
        )
        
    
    lista = Receta.objects.all().order_by('-id')
    
    return render(request, "home.html",{'lista': lista})


def eliminarReceta(request):
    deleteId = int(request.POST.get('deleteID'))
    receta = Receta.objects.get(id = deleteId)
        
    receta.delete() 
    
    return redirect("/")
    
def AgregarReceta(request):
    return render(request, "agregarReceta.html")


def RecetaDetalle(request, id):
    
    if request.method == 'POST':
        deleteId = request.POST.get('deleteID')
        medicina = Medicamento.objects.get(id = deleteId)
        
        medicina.delete()
    
    receta = Receta.objects.get(id=id)
    medicinas = Medicamento.objects.filter(receta_id=id).order_by('-id')
    
    return render(request, "recetaDetalle.html", {"receta": receta, "medicinas": medicinas})

def AgregarMedicina(request):
    Medicamento.objects.create(
        nombre = request.POST.get("nombre"),
        cantidad = request.POST.get("cantidad"),
        cada = request.POST.get("cada"),
        durante = request.POST.get("durante"),
        receta_id = request.POST.get("recetaId"),
    )
    
    return JsonResponse({
        'status' : 'ok'
    })
    
def actualizar_efectividad(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        nueva_efectividad = data.get("efectividad", 0)

        try:
            receta = Receta.objects.get(id=id)
            receta.efectividad = nueva_efectividad
            receta.save()
            return JsonResponse({"success": True, "efectividad": receta.efectividad})
        except Receta.DoesNotExist:
            return JsonResponse({"success": False, "error": "Receta no encontrada"})

    return JsonResponse({"success": False, "error": "Método no permitido"})