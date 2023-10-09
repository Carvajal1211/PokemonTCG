from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from django.db.models import OuterRef, Subquery
from core.models import *
from decimal import Decimal

class CrearReceta(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):

        tipo_receta = TipoReceta.objects.get(id=request.data["tipo_receta"])

        receta = Receta.objects.create(
            nombre=request.data["nombre"],
            gramaje_receta=request.data["gramaje_receta"],
            tipo_receta=tipo_receta,
            proteina=request.data["ptj_proteina"],
            salsa=request.data["ptj_salsa"],
            guarnicion=request.data["ptj_guarnicion"],
        )

        familia = Familia.objects.get(nombre__icontains="Preparación")

        producto = Producto.objects.create(
            familia=familia,
            codigo=None,
            unidad_medida=3,
            cantidad_medida=400,
            nombre=request.data["nombre"]
        )

        return Response(
            {"HTTP_200_OK": "¡Datos Ingresados Correctamente!"},
                status=status.HTTP_200_OK
            )
    
    def get(self, request):
        return Response("200")

class EditarReceta(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}
        tipo_receta = TipoReceta.objects.get(id=request.data["id_tipo_receta"])

        receta = Receta.objects.filter(id=request.data["id_receta"]).update(
            nombre=request.data["nombre"],
            gramaje_receta=request.data["gramaje_receta"],
            tipo_receta=tipo_receta,
            ptj_proteina=request.data["ptj_proteina"],
            ptj_salsa=request.data["ptj_salsa"],
            ptj_guarnicion=request.data["ptj_guarnicion"],
        )
            
        return Response(response)
    
class EliminarReceta(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}
        producto = Producto.objects.filter(pk=request.data["id_receta"]).delete()
        return Response(response)

class FilterRecetas(APIView):
    # authentication_classes = []
    # permissions_classes = []

    def post(self, request, format=None):
        response = {}
        query = Q()

        if request.data["select_nombre"]:
            query &= Q(nombre__icontains=request.data["select_nombre"])
        
        recetas = Receta.objects.filter(query)

        response["recetas"] = [{
            "nombre": receta.nombre,
            "gramaje_receta": receta.gramaje_receta,
            "tipo_receta": receta.tipo_receta.nombre,
            "id_tipo_receta": receta.tipo_receta.id,
            "id_receta": receta.id,
            "ptj_proteina": receta.proteina,
            "ptj_salsa": receta.salsa,
            "ptj_guarnicion": receta.guarnicion,
        } for receta in recetas]

    
        return Response(response["recetas"])

class GetIngredientes(APIView):
    def post(self, request, format=None):
        response = {}
        
        receta_id = request.data.get('id_receta')  # Obten el id de la receta desde los datos de la solicitud

        try:
            receta = Receta.objects.get(id=receta_id)
            print(receta, "receta")
        except Receta.DoesNotExist:
            return Response({"error": "Receta no encontrada"}, status=404)

        productos_gramaje = receta.producto_gramaje.all()

        response["recetas"] = [{
            "id_producto": producto['id'],
            "producto": producto['producto__id'],  # Acceso al campo id del modelo relacionado
            "gramaje": producto['gramaje'],
        } for producto in productos_gramaje.values('id', 'producto__id', 'gramaje')]  # Acceso al campo id del modelo relacionado

        return Response(response["recetas"])
    
class UpdateRecetas(APIView):
    def post(self, request, format=None):
        response = {}
    
        id_receta = request.data['id_receta']
        recetas_data = request.data['recetas']
        
        try:
            receta = Receta.objects.get(id=id_receta)
        except Receta.DoesNotExist:
            return Response({"error": "Receta no encontrada"}, status=404)

        relaciones_existentes = receta.producto_gramaje.all()
        existing_ids = set(relacion.producto.id for relacion in relaciones_existentes)
        
        for receta_info in recetas_data:
            nuevo_gramaje = receta_info['gramaje']
            id_producto = receta_info['id_producto']
            
            if id_producto in existing_ids:
                producto_gramaje = ProductoGramaje.objects.get(producto__id=id_producto, receta=receta)
                producto_gramaje.gramaje = nuevo_gramaje
                producto_gramaje.save()
                existing_ids.remove(id_producto)
            else:
                producto_gramaje = ProductoGramaje.objects.create(
                    producto_id=id_producto,
                    gramaje=nuevo_gramaje
                )
                receta.producto_gramaje.add(producto_gramaje)
        
        # Eliminar relaciones no presentes en el JSON
        for id_producto in existing_ids:
            producto_gramaje = ProductoGramaje.objects.get(producto__id=id_producto, receta=receta)
            receta.producto_gramaje.remove(producto_gramaje)
        
        response['success'] = True

        return Response(response)

class CalcularReceta(APIView):
    def post(self, request, format=None):
        response = {}

        receta = Receta.objects.get(id=request.data["receta"])
        gramaje = int(request.data["gramaje"])
        cantidad = int(request.data["cantidad"])

        proteina = Decimal(receta.proteina)
        salsa = Decimal(receta.salsa)
        guarnicion = Decimal(receta.guarnicion)
        nombre = receta.nombre

        total_proteina = gramaje * (proteina / 100) * cantidad
        total_salsa = gramaje * (salsa / 100) * cantidad
        total_guarnicion = gramaje * (guarnicion / 100) * cantidad

        response["receta"] = {
            "nombre": nombre,
            "porcentaje_proteina": proteina,
            "porcentaje_salsa": salsa,
            "porcentaje_guarnicion": guarnicion,
            "total_proteina": total_proteina,
            "total_salsa": total_salsa,
            "total_guarnicion": total_guarnicion,
        }

        return Response(response["receta"])
