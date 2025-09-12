from django.db import models
import datetime
from django.utils import timezone
# Create your models here.

class Receta(models.Model):
    doc = models.CharField(max_length=255) 
    fecha = models.DateField()
    efectividad = models.IntegerField(default=0) 
    activo = models.BooleanField(default=False)
    lugar = models.CharField(null=True)
    
    def __str__(self):
        return f"Receta {self.id} - {self.doc}"
    
    def cantidad_medicinas(self):
        return self.medicamentos.count()

class Medicamento(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='medicamentos')
    nombre = models.CharField(max_length=255)
    cantidad = models.CharField(max_length=50)  
    cada = models.CharField(max_length=50)     
    durante = models.CharField(max_length=50)
    img = models.ImageField(upload_to='imagenes')  

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"