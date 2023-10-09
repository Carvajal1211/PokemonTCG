from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from django.db.models import OuterRef, Subquery
from core.models import *

class CrearStock(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):

        producto = Producto.objects.get(id=request.data["producto"])
        bodega = Bodega.objects.get(id=request.data["bodega"])

        producto = Producto.objects.create(
            producto=producto,
            bodega=bodega,
            cantidad=request.data["cantidad"],
            cantidad_medida=request.data["cantidad_medida"],
        )

        return Response(
            {"HTTP_200_OK": "¡Datos Ingresados Correctamente!"},
                status=status.HTTP_200_OK
            )

    def get(self, request):
        return Response("200")

class EditarStock(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}

        producto = Producto.objects.get(id=request.data["producto"])
        bodega = Bodega.objects.get(id=request.data["bodega"])

        stock = Stock.objects.filter(pk=request.data["id_stock"])[0]
        stock.producto=producto
        stock.bodega=bodega
        stock.cantidad=request.data["cantidad"]
        stock.cantidad_medida=request.data["cantidad_medida"]
        stock.save()

        return Response(response)
    
class EliminarStock(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}
        stock = Stock.objects.filter(pk=request.data["id_stock"]).delete()
        return Response(response)

class FilterStock(APIView):
    # authentication_classes = []
    # permissions_classes = []

    def post(self, request, format=None):
        response = {}
        query = Q()

        if request.data["select_producto"]:
            query &= Q(producto__nombre=request.data["select_producto"])
        if request.data["select_bodega"]:
            query &= Q(bodega__nombre__icontains=request.data["select_bodega"])
        
        stocks = Bodega.objects.filter(query)

        response["stocks"] = [{
            # Producto
            "prod_nombre": stock.producto.nombre,
            "prod_medida": stock.producto.cantidad_medida,
            "prod_sku": stock.producto.codigo,
            "prod_id": stock.producto.id,
            # Bodega
            "bodega_nombre": stock.unidad_medida,
            "bodega_id": stock.cantidad_medida,
            # Stock
            "cantidad": stock.id,
            "cantidad_medida": stock.id,
            "stock_id": stock.id,
        } for stock in stocks]

    
        return Response(response["stocks"])

#####################

class GetStock(APIView):
    # authentication_classes = []
    # permissions_classes = []

    def post(self, request, format=None):
        response = {}

        stocks = Stock.objects.filter(bodega__id=request.data["id_bodega"])

        response["stocks"] = [{
            "producto": stock.producto.nombre,
            "cantidad": stock.cantidad,
            "unidad_medida": stock.producto.unidad_medida,
            "cantidad_medida": stock.producto.cantidad_medida,
            "id_stock": stock.id,
        } for stock in stocks]

    
        return Response(response["stocks"])