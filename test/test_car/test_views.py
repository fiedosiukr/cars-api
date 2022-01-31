from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.car.models import Car, Rate


class CarViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.car_list_url = reverse("car-list")
        cls.car_1 = Car.objects.create(make="Volkswagen", model="Golf")
        cls.car_2 = Car.objects.create(make="Volkswagen", model="Passat")
        cls.car_1_detail_url = reverse("car-detail", kwargs={"pk": cls.car_1.pk})

        Rate.objects.bulk_create((Rate(car=cls.car_1, rating=5), Rate(car=cls.car_1, rating=3)))

        cls.existing_car_data = {"make": "Volkswagen", "model": "Golf"}
        cls.car_exists_response_json = {
            "Results": [{"Make_Name": "Audi", "Model_Name": "RS3"}, {"Make_Name": "AUDI", "Model_Name": "A3"}],
            "Message": "Random message",
            "Count": 2,
        }
        cls.car_does_not_exist_response_json = {"Results": [], "Message": "Random message", "Count": 0}

    def test_create_existing_car(self):
        response = self.client.post(path=self.car_list_url, data=self.existing_car_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 2)

    @mock.patch("src.apps.car.services.requests.get")
    def test_create_new_car_and_car_does_not_exist(self, request_mock):
        request_mock.return_value.json.return_value = self.car_exists_response_json

        response = self.client.post(path=self.car_list_url, data={"make": "Audi", "model": "A3"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 3)

    @mock.patch("src.apps.car.services.requests.get")
    def test_create_new_car_and_car_exists(self, request_mock):
        request_mock.return_value.json.return_value = self.car_does_not_exist_response_json

        response = self.client.post(path=self.car_list_url, data={"make": "Audi", "model": "A3"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Car.objects.count(), 2)

    def test_delete_car(self):
        response = self.client.delete(path=self.car_1_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 1)

    def test_list_cars(self):
        response = self.client.get(path=self.car_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["avg_rating"], 4.0)
        self.assertEqual(response.data[1]["avg_rating"], 0.0)


class PopularCarListViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.car_list_url = reverse("popular-car-list")
        cls.car_1 = Car.objects.create(make="Volkswagen", model="Golf")
        cls.car_2 = Car.objects.create(make="Volkswagen", model="Passat")

        Rate.objects.bulk_create((Rate(car=cls.car_1, rating=5), Rate(car=cls.car_1, rating=3)))

    def test_popular_car_list(self):
        response = self.client.get(path=self.car_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["rates_number"], 2)
        self.assertEqual(response.data[1]["rates_number"], 0)


class RateCarViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rate_car_url = reverse("rate-car")
        cls.car_1 = Car.objects.create(make="Volkswagen", model="Golf")
        cls.car_2 = Car.objects.create(make="Volkswagen", model="Passat")

        cls.invalid_payload_1 = {"car_id": cls.car_1.pk, "rating": 6}
        cls.invalid_payload_2 = {"car_id": cls.car_2.pk, "rating": 2.5}
        cls.valid_payload = {"car_id": cls.car_1.pk, "rating": 4}

    def test_rate_car_invalid_payload(self):
        with self.subTest("Rating greater than 5 returns bad request."):
            response = self.client.post(path=self.rate_car_url, data=self.invalid_payload_1)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Rate.objects.filter(car=self.car_1).count(), 0)

        with self.subTest("Non-integer rating returns bad request."):
            response = self.client.post(path=self.rate_car_url, data=self.invalid_payload_1)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Rate.objects.filter(car=self.car_2).count(), 0)

    def test_create_car_valid_payload(self):
        response = self.client.post(path=self.rate_car_url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rate.objects.filter(car=self.car_1).count(), 1)
