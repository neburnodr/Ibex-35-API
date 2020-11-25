from rest_framework import serializers
from .models import Valor


class ValorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valor
        fields = '__all__'
