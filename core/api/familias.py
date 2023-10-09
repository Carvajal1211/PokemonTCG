from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from core.models import *

class CrearFamilia(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):

        Familia.objects.create(
            nombre=request.data["nombre"],
        )

        return Response(
            {"HTTP_200_OK": "¡Datos Ingresados Correctamente!"},
            status=status.HTTP_200_OK
        )
    
    def get(self, request):
        return Response("200")

class EditarFamilia(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}

        Familia.objects.filter(pk = request.data["id_familia"]).update(
            nombre=request.data["nombre"],
        )
        return Response(response)
    
class EliminarFamilia(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}
        Familia.objects.filter(pk=request.data["id_familia"])[0].delete()
       
        return Response(response)

class FilterFamilia(APIView):
    # authentication_classes = []
    # permissions_classes = []

    def post(self, request, format=None):
        response = {}
        query = Q()
        if request.data["select_nombre"]:
            query &= Q(nombre__icontains=request.data["select_nombre"])
        
        familias = Familia.objects.filter(query)

        response["familias"] = [{
            "nombre": familia.nombre,
            "id_familia": familia.id,
        } for familia in familias]

        return Response(response["familias"])