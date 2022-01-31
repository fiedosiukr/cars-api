from django.test import TestCase
from pydantic import ValidationError

from src.apps.car.entities import CarEntity


class CarEntityTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.car_1 = CarEntity(make_name="Volkswagen", model_name="Golf")
        cls.car_2 = CarEntity(make_name="VoLkSwAgEn", model_name="gOLF")
        cls.valid_data_1 = {"Make_Name": "Volkswagen", "Model_Name": "Golf"}
        cls.valid_data_2 = {"make_name": "Volkswagen", "model_name": "Golf"}
        cls.invalid_data = {"makename": "Volkswagen", "modelname": "Golf"}

    def test_two_cars_equal(self):
        self.assertEqual(self.car_1, self.car_2)

    def test_create_car_entity_valid(self):
        with self.subTest("CarEntity is created with upper case letters."):
            car_entity = CarEntity(**self.valid_data_1)

            self.assertEqual(car_entity.dict(), self.valid_data_2)

        with self.subTest("CarEntity is created with all lower case letters."):
            car_entity = CarEntity(**self.valid_data_2)

            self.assertEqual(car_entity.dict(), self.valid_data_2)

    def test_create_car_entity_invalid(self):
        with self.assertRaises(ValidationError):
            car_entity = CarEntity(**self.invalid_data)
