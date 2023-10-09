from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from core.models import *

class CrearBodega(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):

        Bodega.objects.create(
            nombre=request.data["nombre"],
        )

        return Response(
            {"HTTP_200_OK": "¡Datos Ingresados Correctamente!"},
            status=status.HTTP_200_OK
        )
    
    def get(self, request):
        return Response("200")

class EditarBodega(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}

        Bodega.objects.filter(pk = request.data["id_bodega"]).update(
            nombre=request.data["nombre"],
        )
        return Response(response)
    
class EliminarBodega(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}
        Bodega.objects.filter(pk=request.data["id_bodega"])[0].delete()
       
        return Response(response)

class FilterBodega(APIView):
    # authentication_classes = []
    # permissions_classes = []

    def post(self, request, format=None):
        response = {}
        query = Q()
        if request.data["select_nombre"]:
            query &= Q(nombre__icontains=request.data["select_nombre"])
        
        bodegas = Bodega.objects.filter(query)

        response["bodegas"] = [{
            "nombre": bodega.nombre,
            "id_bodega": bodega.id,
        } for bodega in bodegas]

        return Response(response["bodegas"])