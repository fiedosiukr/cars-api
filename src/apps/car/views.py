from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.apps.car.entities import CarEntity
from src.apps.car.models import Car, Rate
from src.apps.car.serializers import (
    CarSerializer,
    PopularCarSerializer,
    RateCarSerializer,
)
from src.apps.car.services import CarService


class CarViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.with_avg_rating().order_by("-avg_rating")

    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        car = CarService.create_car(
            car_entity=CarEntity(
                make_name=serializer.validated_data["make"], model_name=serializer.validated_data["model"]
            )
        )

        return Response(data=self.get_serializer(car).data, status=status.HTTP_201_CREATED)


class PopularCarListView(ListAPIView):
    serializer_class = PopularCarSerializer
    queryset = Car.objects.by_most_popular()


class RateCarView(CreateAPIView):
    serializer_class = RateCarSerializer
    queryset = Rate.objects.all()

    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        car = get_object_or_404(Car, id=serializer.validated_data.pop("car_id"))
        rate = Rate.objects.create(car=car, **serializer.validated_data)

        return Response(data=self.get_serializer(rate).data, status=status.HTTP_201_CREATED)
