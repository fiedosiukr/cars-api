from rest_framework import serializers

from src.apps.car.models import Car, Rate


class CarSerializer(serializers.ModelSerializer):
    avg_rating = serializers.DecimalField(max_digits=2, decimal_places=1, read_only=True)

    class Meta:
        model = Car
        fields = ("id", "make", "model", "avg_rating")


class PopularCarSerializer(serializers.ModelSerializer):
    rates_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = ("id", "make", "model", "rates_number")


class RateCarSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField()

    class Meta:
        model = Rate
        fields = ("car_id", "rating")
