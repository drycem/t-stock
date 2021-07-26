from rest_framework import serializers

from .models import Urunler, Islemler

class UrunlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urunler
        fields = '__all__'


class IslemlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Islemler
        fields = '__all__'
