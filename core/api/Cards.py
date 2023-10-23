from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from core.models import *
from django.http import JsonResponse
from django.views import View
import json






class CrearCartaAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        nombre = request.data.get('nombre')
        rareza_nombre = request.data.get('rareza')
        version_nombre = request.data.get('version')
        precio = request.data.get('precio')

        try:
            carta, created = Carta.objects.get_or_create(nombre=nombre)
        except Carta.DoesNotExist:
            carta = Carta(nombre=nombre)
            carta.save()

        try:
            rareza, created = Rareza.objects.get_or_create(nombre=rareza_nombre)
        except Rareza.DoesNotExist:
            rareza = Rareza(nombre=rareza_nombre)
            rareza.save()

        try:
            version, created = Version.objects.get_or_create(nombre=version_nombre)
        except Version.DoesNotExist:
            version = Version(nombre=version_nombre)
            version.save()

        precio, created = Precio.objects.get_or_create(carta=carta, rareza=rareza, version=version, precio=precio)

        return Response({'message': 'Carta creada exitosamente'}, status=status.HTTP_201_CREATED)


