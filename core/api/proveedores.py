from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from core.models import *

class CrearProveedor(APIView):
    def post(self, request):

        Proveedor.objects.create(
            nombre_empresa=request.data["nombre_empresa"],
            persona_cargo=request.data["persona_cargo"],
            correo=request.data["correo"],
            telefono=request.data["telefono"],
        )

        return Response(
            {"HTTP_200_OK": "¡Datos Ingresados Correctamente!"},
            status=status.HTTP_200_OK
        )
    
    def get(self, request):
        return Response("200")

class EditarProveedor(APIView):
    def post(self, request):
        response = {}

        Proveedor.objects.filter(pk = request.data["id_proveedor"]).update(
            nombre_empresa=request.data["nombre_empresa"],
            persona_cargo=request.data["persona_cargo"],
            correo=request.data["correo"],
            telefono=request.data["telefono"],
        )
        return Response(response)
    
class EliminarProveedor(APIView):
    def post(self, request):
        response = {}
        Proveedor.objects.filter(pk=request.data["id_proveedor"])[0].delete()
       
        return Response(response)

class FilterProveedores(APIView):
    def post(self, request, format=None):
        response = {}
        query = Q()
        if len(request.data["select_nombre_empresa"]) >= 3:
            query &= Q(nombre_empresa__icontains=request.data["select_nombre_empresa"])
        if len(request.data["select_persona_cargo"]) >= 3:
            query &= Q(persona_cargo__icontains=request.data["select_persona_cargo"])
        
        proveedores = Proveedor.objects.filter(query)

        response["proveedores"] = [{
            "nombre_empresa": proveedor.nombre_empresa,
            "persona_cargo": proveedor.persona_cargo,
            "correo": proveedor.correo,
            "telefono": proveedor.telefono,
            "id_proveedor": proveedor.id,
        } for proveedor in proveedores]

        return Response(response["proveedores"])

class FilterGetProveedores(APIView):
    def post(self, request, format=None):
        response = {}

        proveedores = Proveedor.objects.all().order_by('nombre_empresa')

        response["proveedores"] = [{
            "name": proveedor.nombre_empresa,
            "id": proveedor.id,
        } for proveedor in proveedores]

        return Response(response["proveedores"])


#########################

class GetProveedores(APIView):
    def post(self, request, format=None):
        response = {}
        
        proveedores = ProveedorPrecio.objects.filter(producto__id=request.data['id_producto'])

        response["proveedores"] = [{
                "precio":proveedor.precio  ,
                "id_precio":proveedor.id,
                "proveedor":proveedor.proveedor.nombre_empresa,
                "id_proveedor":proveedor.proveedor.id,
        }for proveedor in proveedores ]

        return Response(response["proveedores"])

class UpdateProveedores(APIView):
    def post(self, request, format=None):
        response = {}
    
        id_producto = request.data['id_producto']
        proveedores_data = request.data['proveedores']
        
        # Obtener relaciones existentes en el backend
        relaciones_existentes = ProveedorPrecio.objects.filter(
            producto__id=id_producto
        )
        
        # Crear una lista de IDs de proveedores seleccionados en el front
        ids_proveedores_seleccionados = [prov['id_proveedor'] for prov in proveedores_data]
        
        # Eliminar relaciones que están en el backend pero no en el front
        for relacion_existente in relaciones_existentes:
            if relacion_existente.proveedor_id not in ids_proveedores_seleccionados:
                relacion_existente.delete()
        
        # Actualizar o crear relaciones según corresponda
        for proveedor_info in proveedores_data:
            id_proveedor = proveedor_info['id_proveedor']
            nuevo_precio = proveedor_info['precio']
            
            proveedor = Proveedor.objects.get(id=id_proveedor)
            
            try:
                # Intentar obtener la relación existente
                proveedor_precio = ProveedorPrecio.objects.get(
                    producto__id=id_producto,
                    proveedor=proveedor,
                )
                
                # Si existe, actualizar el precio
                proveedor_precio.precio = nuevo_precio
                proveedor_precio.save()
            except ProveedorPrecio.DoesNotExist:
                # Si no existe, crear la relación con el precio
                ProveedorPrecio.objects.create(
                    producto_id=id_producto,
                    proveedor=proveedor,
                    precio=nuevo_precio,
                )
            
        response['success'] = True

        return Response(response)