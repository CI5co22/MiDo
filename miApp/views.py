from email.utils import unquote
from django.shortcuts import render, redirect, get_object_or_404
# from .models import Tareas
from django.http import HttpResponse, JsonResponse
from .models import Receta, Medicamento
from cloudinary.uploader import destroy
from cloudinary.uploader import upload

import json
import os



# Create your views here.
def index(request):
    
    if request.method == 'POST':
        Receta.objects.create(
            doc = request.POST.get('doc'),
            fecha = request.POST.get('fecha'),
            lugar = request.POST.get('lugar')
        )
        
    activos =  Receta.objects.filter(activo=True)
   
    
    lista = Receta.objects.filter(activo=False).order_by('-id')
    
    return render(request, "home.html",{'lista': lista, 'activos': activos})


def eliminarReceta(request):
    deleteId = int(request.POST.get('deleteID'))
    receta = Receta.objects.get(id = deleteId)
    
    medicinas = receta.medicamentos.all()  
    
    for med in medicinas:
        if med and med.img:
                try:
                    public_id = med.img.public_id

                    destroy(public_id)
                    print(f"✅ Imagen {public_id} eliminada de Cloudinary")

                except Exception as e:
                    print(f"❌ Error eliminando de Cloudinary: {e}")
                                    
        med.delete()
    
    receta.delete()
    
    return redirect("/")
    
def AgregarReceta(request):
    return render(request, "agregarReceta.html")

def ActivarReceta(request):
    activarID = request.POST.get('id')
    receta = Receta.objects.get(id = activarID)
    
    if receta.activo:
        receta.activo = False
    else:
        receta.activo = True
    
    receta.save()
    
    return JsonResponse({
        'status' : 'ok'
    })
    
    

def RecetaDetalle(request, id):
    
    if request.method == 'POST':
        deleteId = request.POST.get('deleteID')
        if deleteId:
            medicina = Medicamento.objects.filter(id=deleteId).first()
            
            if medicina and medicina.img:
                try:
                    public_id = medicina.img.public_id

                    destroy(public_id)
                    print(f"✅ Imagen {public_id} eliminada de Cloudinary")

                except Exception as e:
                    print(f"❌ Error eliminando de Cloudinary: {e}")
                                    
                medicina.delete()

    
    receta = Receta.objects.get(id=id)
    medicinas = Medicamento.objects.filter(receta_id=id).order_by('-id')
    
    return render(request, "recetaDetalle.html", {"receta": receta, "medicinas": medicinas})

def AgregarMedicina(request):
    if 'img' in request.FILES:
        result = upload(request.FILES['img'])
        cloudinary_url = result['secure_url']
    else:
        cloudinary_url = ''
    
    # Crea el objeto con la URL de Cloudinary
    Medicamento.objects.create(
        nombre=request.POST.get("nombre"),
        cantidad=request.POST.get("cantidad"),
        cada=request.POST.get("cada"),
        durante=request.POST.get("durante"),
        receta_id=request.POST.get("recetaId"),
        img=cloudinary_url  # URL directa de Cloudinary
    )

    return JsonResponse({
        'status' : 'ok'
    })
    
def editarMedicina(request):    
    recetaID = request.POST.get('recetaID')
    editID = int(request.POST.get('edit-id'))
    medicina = Medicamento.objects.get(id = editID)
    
    if 'img' in request.FILES:
        result = upload(request.FILES['img'])
        cloudinary_url = result['secure_url']
    else:
        cloudinary_url = medicina.img
    
    medicina.nombre = request.POST.get('nombre')
    medicina.cantidad = request.POST.get('cantidad')
    medicina.cada = request.POST.get('cada')
    medicina.durante = request.POST.get('durante')
    medicina.img = cloudinary_url
    medicina.save()
    
    return redirect("receta-detalle", id = recetaID)

def editarReceta(request):
    recetaID = request.POST.get('recetaID')
    receta = Receta.objects.get(id = recetaID)
    
    receta.doc = request.POST.get('doc')
    receta.lugar = request.POST.get('lugar')
    receta.fecha = request.POST.get('fecha')
    receta.save()
    
    return redirect("receta-detalle", id = recetaID)

    
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