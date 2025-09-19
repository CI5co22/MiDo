from email.utils import unquote
from django.shortcuts import render, redirect, get_object_or_404
# from .models import Tareas
from django.http import HttpResponse, JsonResponse
from .models import Receta, Medicamento
from cloudinary.uploader import destroy
from cloudinary.uploader import upload
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import logging

logger = logging.getLogger(__name__)

import json
import os
import threading


# Create your views here.
def index(request):
    
    if request.method == 'POST':
        Receta.objects.create(
            doc = request.POST.get('doc'),
            fecha = request.POST.get('fecha'),
            lugar = request.POST.get('lugar')
        )
        messages.success(request, 'Receta agregada correctamente!')
        
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
                    public_id = med.img_id

                    destroy(public_id)
            
                except Exception as e:
                    print(f"❌ Error eliminando de Cloudinary: {e}")
                                    
        med.delete()
    
    receta.delete()
    messages.success(request, 'Receta eliminada correctamente!')
    
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
                    public_id = medicina.img_id

                    destroy(public_id)

                except Exception as e:
                    print(f"❌ Error eliminando de Cloudinary: {e}")
                                    
        medicina.delete()
        messages.success(request, '¡Medicina eliminada correctamente!')

    
    receta = Receta.objects.get(id=id)
    medicinas = Medicamento.objects.filter(receta_id=id).order_by('-id')
    
    return render(request, "recetaDetalle.html", {"receta": receta, "medicinas": medicinas})


@csrf_exempt
def AgregarMedicina(request):
    try:
        # Validar método
        if request.method != 'POST':
            return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

        # Validar Content-Type para multipart
        if not request.content_type.startswith('multipart/form-data'):
            return JsonResponse({'status': 'error', 'message': 'Formato de datos inválido'}, status=400)

        # Validar tamaño total de la petición
        content_length = request.META.get('CONTENT_LENGTH', 0)
        if content_length:
            content_length = int(content_length)
            if content_length > 50 * 1024 * 1024:  # 50MB máximo
                return JsonResponse({'status': 'error', 'message': 'Petición demasiado grande'}, status=413)

        cloudinary_url = ''
        public_id = ''

        # Procesar imagen de forma segura
        if 'img' in request.FILES:
            img_file = request.FILES['img']
            
            # Validaciones del archivo
            if not img_file:
                return JsonResponse({'status': 'error', 'message': 'Archivo de imagen inválido'}, status=400)
            
            if img_file.size > 10 * 1024 * 1024:  # 10MB máximo por imagen
                return JsonResponse({'status': 'error', 'message': 'Imagen demasiado grande (máx 10MB)'}, status=400)
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if hasattr(img_file, 'content_type') and img_file.content_type not in allowed_types:
                return JsonResponse({'status': 'error', 'message': 'Tipo de imagen no permitido'}, status=400)
            
            try:
                # Intentar leer un poco del archivo para verificar que no está corrupto
                img_file.seek(0)
                test_read = img_file.read(1024)  # Leer primeros 1KB
                if not test_read:
                    return JsonResponse({'status': 'error', 'message': 'Archivo de imagen vacío'}, status=400)
                img_file.seek(0)  # Volver al inicio
                
                # Subir a Cloudinary
                result = upload(img_file)
                cloudinary_url = result['secure_url']
                public_id = result['public_id']
                
            except Exception as e:
                logger.error(f"Error subiendo imagen: {str(e)}")
                return JsonResponse({'status': 'error', 'message': 'Error procesando imagen'}, status=500)

        # Validar campos requeridos
        required_fields = ['nombre', 'cantidad', 'cada', 'durante', 'recetaId']
        for field in required_fields:
            if not request.POST.get(field):
                return JsonResponse({'status': 'error', 'message': f'Campo {field} requerido'}, status=400)

        # Crear medicamento
        Medicamento.objects.create(
            nombre=request.POST.get("nombre"),
            cantidad=request.POST.get("cantidad"),
            cada=request.POST.get("cada"),
            durante=request.POST.get("durante"),
            receta_id=request.POST.get("recetaId"),
            img=cloudinary_url,
            img_id=public_id
        )
        
        messages.success(request, '¡Medicina agregada correctamente!')

        return JsonResponse({'status': 'ok'})

    except Exception as e:
        logger.error(f"Error en AgregarMedicina: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error interno'}, status=500)

@csrf_exempt 
def editarMedicina(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

        recetaID = request.POST.get('recetaID')
        editID = int(request.POST.get('edit-id'))
        medicina = Medicamento.objects.get(id=editID)
        
        old_public_id = medicina.img_id
        cloudinary_url = medicina.img
        public_id = medicina.img_id

        # Procesar nueva imagen si existe
        if 'img' in request.FILES:
            img_file = request.FILES['img']
            
            # Mismas validaciones que en AgregarMedicina
            if not img_file or img_file.size > 10 * 1024 * 1024:
                return redirect("receta-detalle", id=recetaID)
            
            try:
                # Verificar archivo
                img_file.seek(0)
                test_read = img_file.read(1024)
                if not test_read:
                    return redirect("receta-detalle", id=recetaID)
                img_file.seek(0)
                
                # Subir nueva imagen
                result = upload(img_file)
                cloudinary_url = result['secure_url']
                public_id = result['public_id']
                
                # Eliminar imagen anterior
                if old_public_id:
                    try:
                        destroy(old_public_id)
                    except Exception as e:
                        logger.warning(f"No se pudo eliminar imagen anterior: {e}")
                        
            except Exception as e:
                logger.error(f"Error procesando imagen en edición: {str(e)}")
                # Continuar sin cambiar imagen
                pass

        # Actualizar medicamento
        medicina.nombre = request.POST.get('nombre')
        medicina.cantidad = request.POST.get('cantidad')
        medicina.cada = request.POST.get('cada')
        medicina.durante = request.POST.get('durante')
        medicina.img = cloudinary_url
        medicina.img_id = public_id
        medicina.save()
        messages.success(request, '¡Medicina actualizada!')
        
        return redirect("receta-detalle", id=recetaID)
        
    except Exception as e:
        logger.error(f"Error en editarMedicina: {str(e)}")
        return redirect("receta-detalle", id=request.POST.get('recetaID', 1))

def editarReceta(request):
    recetaID = request.POST.get('recetaID')
    receta = Receta.objects.get(id = recetaID)
    
    receta.doc = request.POST.get('doc')
    receta.lugar = request.POST.get('lugar')
    receta.fecha = request.POST.get('fecha')
    receta.save()
    messages.success(request, 'Receta actualizada!')
    
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