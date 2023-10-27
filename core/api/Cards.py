from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from core.models import *
from django.http import JsonResponse
from django.views import View
import json
from django.db.models import Min
from django.contrib.auth.decorators import login_required




class VerificarExistenciaEnBaseDeDatos(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        code = request.data.get('code', None)

        if code:
            try:
                # Busca todos los precios de cartas con el mismo código
                precios = Precio.objects.filter(code=code)

                if precios.exists():
                    # Si hay precios, obtén el más bajo
                    precio_mas_bajo = precios.aggregate(Min('precio'))['precio__min']
                    return Response({'precio_mas_bajo': precio_mas_bajo})
                else:
                    # Si no hay precios, puedes devolver un valor por defecto o un mensaje de error
                    return Response({'Erro del precio bajo': None})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Código no proporcionado en la solicitud.'}, status=status.HTTP_BAD_REQUEST)
        

class CrearCartaAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        nombre = request.data.get('nombre')
        rareza_nombre = request.data.get('rareza')
        version_nombre = request.data.get('version')
        precio = request.data.get('precio')
        imagen = request.data.get('imagen')  # Campo de imagen
        code = request.data.get('code')  # Campo de código
        user = request.data.get('usuario_id')

        usuario = User.objects.get(id=user)
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

        # Crear un nuevo objeto Precio con todos los campos
        precio, created = Precio.objects.get_or_create(
            usuario = usuario,
            carta=carta,
            rareza=rareza,
            version=version,
            precio=precio,
            imagen=imagen, 
            code=code
        )

        return Response({'message': 'Carta creada exitosamente'}, status=status.HTTP_201_CREATED)
    
class PreciosPorCodigo(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        # Obtén el código del cuerpo de la solicitud
        code = request.data.get('code')

        # Busca todos los precios relacionados con el código
        precios = Precio.objects.filter(code=code).values('precio', 'fecha_publicacion')

        return Response(list(precios), status=status.HTTP_200_OK)


