from django.http import JsonResponse

from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_f
from django.contrib.auth import logout, authenticate

import requests
from django.views import View
import json
from core.models import *
# Create your views here.

def login(request):
    template_name = "login.html"
    context = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        # Obtener el valor de la opción "Recuérdame"
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)
            login_f(request, user)
            if user.is_superuser:
                return redirect("pokemon_tcg/")
            return redirect("pokemon_tcg/")
        else:
            logout(request)
    context['remember_me'] = request.POST.get('remember_me')
    return render(request, template_name, context)

@login_required
def index(request):
    template_name = "base.html"
    context = {}
    return render(request, template_name, context)

@login_required
def Pokemon_tcg(request):
    template_name = "pokemon_tcg.html"
    context = {}
    return render(request, template_name, context)

@login_required
def Pokemon_battle(request):
    template_name = "pokemon_battle.html"
    context = {}
    return render(request, template_name, context)

@login_required
def Pokemon(request):
    template_name = "pokemon.html"
    context = {}
    return render(request, template_name, context)

@login_required
def CreadorCarta(request):
    template_name = "crear_carta.html"
    context = {}
    return render(request, template_name, context)


