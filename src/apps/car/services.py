import requests
from rest_framework import status

from src.apps.car.entities import CarEntity, ResponseEntity
from src.apps.car.exceptions import CarAPIUnavailableException, CarNotFoundException
from src.apps.car.models import Car


class CarService:
    _base_url = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json"

    @classmethod
    def create_car(cls, car_entity: CarEntity) -> Car:
        if (
            car := Car.objects.filter(make__iexact=car_entity.make_name, model__iexact=car_entity.model_name).first()
        ) is not None:
            return car

        response_entity = cls._fetch_models_for_make(make=car_entity.make_name)
        if response_entity.count and cls._car_exists(car_entity=car_entity, cars=response_entity.results):
            return Car.objects.create(make=car_entity.make_name.capitalize(), model=car_entity.model_name.capitalize())

        raise CarNotFoundException

    @classmethod
    def _fetch_models_for_make(cls, make: str) -> ResponseEntity:
        try:
            response = requests.get(cls._get_base_url(make=make))
        except requests.RequestException:
            raise CarAPIUnavailableException

        return ResponseEntity(**response.json())

    @classmethod
    def _car_exists(cls, car_entity: CarEntity, cars: list[CarEntity]) -> bool:
        return any(car_entity == car for car in cars)

    @classmethod
    def _get_base_url(cls, make: str) -> str:
        return cls._base_url.format(make)
