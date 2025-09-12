from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('receta/<int:id>/', views.RecetaDetalle),
    path('receta/agregar/', views.AgregarMedicina),
    path('receta/activar/', views.ActivarReceta),
    path('actualizar-efectividad/<int:id>/',views.actualizar_efectividad),
    path('eliminarReceta/',views.eliminarReceta)
]
