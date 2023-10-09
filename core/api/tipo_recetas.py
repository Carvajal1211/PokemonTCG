from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from core.models import *

class CrearTipoReceta(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):

        TipoReceta.objects.create(
            nombre=request.data["nombre"],
        )

        return Response(
            {"HTTP_200_OK": "¡Datos Ingresados Correctamente!"},
            status=status.HTTP_200_OK
        )
    
    def get(self, request):
        return Response("200")

class EditarTipoReceta(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}

        TipoReceta.objects.filter(pk = request.data["id_receta"]).update(
            nombre=request.data["nombre"],
        )
        return Response(response)
    
class EliminarTipoReceta(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}
        TipoReceta.objects.filter(pk=request.data["id_receta"])[0].delete()
       
        return Response(response)

class FilterTipoRecetas(APIView):
    # authentication_classes = []
    # permissions_classes = []

    def post(self, request, format=None):
        response = {}
        query = Q()
        if request.data["select_nombre"]:
            query &= Q(nombre__icontains=request.data["select_nombre"])
        
        tipo_receta = TipoReceta.objects.filter(query)

        response["tipo_receta"] = [{
            "nombre": receta.nombre,
            "id_receta": receta.id,
        } for receta in tipo_receta]

        return Response(response["tipo_receta"])