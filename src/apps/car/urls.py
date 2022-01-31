from django.urls import path
from rest_framework.routers import DefaultRouter

from src.apps.car.views import CarViewSet, PopularCarListView, RateCarView

urlpatterns = [
    path("popular/", PopularCarListView.as_view(), name="popular-car-list"),
    path("rate/", RateCarView.as_view(), name="rate-car"),
]

router = DefaultRouter()
router.register("cars", CarViewSet, basename="car")

urlpatterns += router.urls
