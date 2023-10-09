from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework import authentication, permissions
from core.models import *

class CreateTekUser(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        user = User.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            email=request.data["email"],
            username=request.data["email"],
            password=request.data["password"],
        )
        user.set_password(request.data["password"])
        user.save()
        usuario = TeckUser.objects.create(
            user=user,
            rut=request.data["rut"],
            user_type=request.data["user_type"],
        )
        usuario.save()
        return Response(
            {"HTTP_200_OK": "¡Datos Ingresados Correctamente!", "user_id":user.pk, "tekchef_user_id": usuario.pk},
                status=status.HTTP_200_OK
            )
    
    def get(self, request):
        return Response("200")

class EditTekUser(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}

        User.objects.filter(pk = request.data["id_user"]).update(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            email=request.data["email"],
            username=request.data["email"]
        )
        TeckUser.objects.filter(pk = request.data["tekchef_user_id"]).update(
            user_type = request.data["user_type"],
            rut = request.data["rut"],
        )
        return Response(response)
    
class SoftDeleteTekUser(APIView):
    # authentication_classes = []
    # permission_classes = []

    def post(self, request):
        response = {}
        # tek_user = TekUser.objects.get(pk=request.data["tek_user_id"]).delete()
        user = User.objects.filter(pk=request.data["id_user"])[0]
        user.is_active=False
        user.save()
        return Response(response)

class FilterUsers(APIView):
    # authentication_classes = []
    # permissions_classes = []

    def post(self, request, format=None):
        response = {}
        query = Q()

        if request.data["select_type"]:
            query &= Q(user_type=request.data["select_type"])
        if request.data["select_users"]:
            query &= Q(user__first_name__icontains=request.data["select_users"]) # | Q(user__last_name__icontains=request.data["select_users"])) | Q(user__first_name__icontains=F('user__first_name') + Value(' ') + F('user__last_name'))
        
        users = TeckUser.objects.filter(query)

        response["users"] = [{
            "first_name": tek_user.user.first_name,
            "last_name": tek_user.user.last_name,
            "email": tek_user.user.email,
            "user_type": tek_user.user_type,
            "rut": tek_user.rut,
            "id": tek_user.id,
            "user_id": tek_user.user.id,
        } for tek_user in users]

        return Response(response["users"])