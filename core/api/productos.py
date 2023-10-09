from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from django.db.models import OuterRef, Subquery
from core.models import *

class CrearProducto(APIView):
    def post(self, request):

        familia = Familia.objects.get(id=request.data["familia"])
        # proveedor = Proveedor.objects.get(id=request.data["proveedor"])

        producto = Producto.objects.create(
            nombre=request.data["nombre"],
            familia=familia,
            codigo=request.data["sku"],
            unidad_medida=request.data["unidad_medida"],
            cantidad_medida=request.data["cantidad_medida"],
        )
        barcode = BarCode.objects.create(
            barcode=request.data["barcode"],
            producto=producto,
        )
        # precio = ProveedorPrecio.objects.create(
        #     producto=producto,
        #     proveedor=proveedor,
        #     precio=request.data["precio"]
        # )

        return Response(
            {"HTTP_200_OK": "¡Datos Ingresados Correctamente!"},
                status=status.HTTP_200_OK
            )
    
    def get(self, request):
        return Response("200")

class EditarProducto(APIView):
    def post(self, request):
        response = {}
        familia = Familia.objects.get(id=request.data["id_familia"])
        # proveedor = Proveedor.objects.get(id=request.data["id_proveedor"])

        producto = Producto.objects.filter(pk=request.data["id_producto"])[0]
        producto.nombre=request.data["nombre"]
        producto.familia=familia
        producto.codigo=request.data["sku"]
        producto.unidad_medida=request.data["unidad_medida"]
        producto.cantidad_medida=request.data["cantidad_medida"]
        producto.save()

        # precio = ProveedorPrecio.objects.filter(id=request.data["id_precio"])[0]
        # precio.producto=producto
        # precio.proveedor=proveedor
        # precio.precio=request.data["precio"]
        # precio.save()

        if request.data["id_barcode"]:
            barcode = BarCode.objects.filter(pk=request.data["id_barcode"]).update(
                barcode=request.data["barcode"],
            )

        else:
            barcode = BarCode.objects.create(
                barcode=request.data["barcode"],
                producto=producto,
            )

            
        return Response(response)
    
class EliminarProducto(APIView):
    def post(self, request):
        response = {}
        producto = Producto.objects.filter(pk=request.data["id_producto"]).delete()
        return Response(response)

class FilterProducto(APIView):
    def post(self, request, format=None):
        response = {}
        query = Q()

        if request.data["select_product_type"]:
            query &= Q(familia__id=request.data["select_product_type"])
        if request.data["select_nombre"]:
            query &= Q(nombre__icontains=request.data["select_nombre"])
        if len(request.data["select_sku"]) >= 3:
            query &= Q(codigo__icontains=request.data["select_sku"])
        
        productos = Producto.objects.filter(query).exclude(familia__nombre="Preparación")

        barcode_subquery = BarCode.objects.filter(producto=OuterRef('pk')).order_by('pk')
        
        productos_with_barcodes = productos.annotate(
            id_barcode=Subquery(barcode_subquery.values('id')[:1]),
            first_barcode=Subquery(barcode_subquery.values('barcode')[:1]),
            # proveedor_precio_id=Subquery(
            #     ProveedorPrecio.objects.filter(producto=OuterRef('pk'))
            #     .values('id')[:1]
            # ),
            # proveedor_precio_nombre=Subquery(
            #     ProveedorPrecio.objects.filter(producto=OuterRef('pk'))
            #     .values('proveedor__nombre_empresa')[:1]
            # ),
            # proveedor_precio_proveedor_id=Subquery(
            #     ProveedorPrecio.objects.filter(producto=OuterRef('pk'))
            #     .values('proveedor__id')[:1]
            # ),
            # proveedor_precio_precio=Subquery(
            #     ProveedorPrecio.objects.filter(producto=OuterRef('pk'))
            #     .values('precio')[:1]
            # )
        )

        response["productos"] = [{
            "nombre": producto.nombre,
            "familia": producto.familia.nombre,
            "familia_id": producto.familia.id,
            "codigo": producto.codigo,
            "unidad_medida": producto.unidad_medida,
            "cantidad_medida": producto.cantidad_medida,
            "id_producto": producto.id,
            # Barcode
            "barcode":producto.first_barcode if producto.first_barcode else "Sin Registro",
            "id_barcode": producto.id_barcode,
            # Proveedor-Precio
        #    "proveedor": producto.proveedor_precio_nombre if producto.proveedor_precio_nombre else "Sin Registro",
        #     "precio": producto.proveedor_precio_precio if producto.proveedor_precio_precio else 0,
        #     "id_precio": producto.proveedor_precio_id if producto.proveedor_precio_id else None,
        #     "id_proveedor": producto.proveedor_precio_proveedor_id if producto.proveedor_precio_proveedor_id else None,
        } for producto in productos_with_barcodes]

    
        return Response(response["productos"])

# Filtro de Productos en base a Componente "Dropdown"
class FilterGetProductos(APIView):
    def post(self, request, format=None):
        response = {}

        productos = Producto.objects.all()

        response["productos"] = [{
            "name": producto.nombre,
            "id": producto.id,
        } for producto in productos]

        return Response(response["productos"])