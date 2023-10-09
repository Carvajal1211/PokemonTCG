from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from core.models import *

class CrearOrden(APIView):
    def post(self, request):
        try:
            # Obtener el JSON de la solicitud
            stock = request.data.get('show_calculos')

            # Obtener los datos del JSON
            id_producto = stock.get("id_producto")
            cantidad = stock.get("cantidad")

            # Crear un nuevo registro en la tabla Stock sin verificar la existencia de Producto y Bodega
            Stock.objects.create(
                producto_id=id_producto,
                bodega__nombre="Preparación",
                cantidad=cantidad,
            )

            return Response(
                {"HTTP_200_OK": "¡Datos Ingresados Correctamente!"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        return Response("200")
