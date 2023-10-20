from rest_framework import generics,status, filters
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# Create your views here.



