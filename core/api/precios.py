from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from core.models import *

class CrearPrecio(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):

        proveedor = Proveedor.objects.get(id=request.data["id_proveedor"])
        producto = Producto.objects.get(id=request.data["id_producto"])

        ProveedorPrecio.objects.create(
            precio=request.data["precio"],
            proveedor=proveedor,
            producto=producto,
        )

        return Response(
            {"HTTP_200_OK": "¡Datos Ingresados Correctamente!"},
            status=status.HTTP_200_OK
        )
    
    def get(self, request):
        return Response("200")

class EditarPrecio(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}

        Familia.objects.filter(pk = request.data["id_precio"]).update(
            precio=request.data["precio"],
        )

        return Response(response)

class EliminarPrecio(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}
        ProveedorPrecio.objects.filter(pk=request.data["id_precio"])[0].delete()
       
        return Response(response)

class FilterPrecios(APIView):
    # authentication_classes = []
    # permissions_classes = []

    def post(self, request, format=None):
        response = {}
        query = Q()

        if request.data["select_nombre_empresa"]:
            query &= Q(proveedor__nombre_empresa__icontains=request.data["select_nombre_empresa"])
        if request.data["select_producto"]:
            query &= Q(producto__nombre__icontains=request.data["select_producto"])
        
        precios = ProveedorPrecio.objects.filter(query)

        response["precios"] = [{
            "proveedor": precio.proveedor.nombre_empresa,
            "id_proveedor": precio.proveedor.id,
            "producto": precio.producto.nombre,
            "id_producto": precio.producto.id,
            "unidad_medida": precio.producto.unidad_medida,
            "cantidad_medida": precio.producto.cantidad_medida,
            "precio": precio.precio,
            "created_at": precio.created_at.strftime("%d/%m/%Y"),
            "id_precio": precio.id,
        } for precio in precios]

        response["precios"] = sorted(response["precios"], key=lambda x: x["created_at"], reverse=True)

        return Response(response["precios"])
