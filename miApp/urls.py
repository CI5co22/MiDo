from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('receta/<int:id>', views.RecetaDetalle),
]
