from django.shortcuts import render
from rest_framework import generics
from .models import Valor
from .serializers import ValorSerializer


# Create your views here.
class ListValorView(generics.ListAPIView):
    queryset = Valor.objects.all()
    serializer_class = ValorSerializer
