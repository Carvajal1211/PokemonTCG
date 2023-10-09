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
import json
from core.models import *
# Create your views here.



def index(request):
    template_name = "base.html"
    context = {}
    return render(request, template_name, context)



def Pokemon_tcg(request):
    template_name = "pokemon_tcg.html"
    context = {}
    return render(request, template_name, context)

def Pokemon_battle(request):
    template_name = "pokemon_battle.html"
    context = {}
    return render(request, template_name, context)

def Pokemon(request):
    template_name = "pokemon.html"
    context = {}
    return render(request, template_name, context)