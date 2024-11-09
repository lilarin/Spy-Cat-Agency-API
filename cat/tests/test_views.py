from rest_framework import status
from rest_framework.test import APITestCase
from cat.models import SpyCat

class SpyCatViewSetTests(APITestCase):
    def setUp(self):
        self.cat = SpyCat.objects.create(
            name="Agent Whiskers",
            years_of_experience=5,
            breed="Siberian",
            salary="300.00"
        )
        self.list_url = "/api/cat/"
        self.detail_url = f"{self.list_url}{self.cat.id}/"

    def test_create_cat(self):
        data = {
            "name": "Felix",
            "years_of_experience": 3,
            "breed": "Siberian",
            "salary": "400.00"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpyCat.objects.count(), 2)
        self.assertEqual(response.data["name"], "Felix")

    def test_retrieve_cat(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.cat.name)

    def test_partial_update_salary(self):
        data = {"salary": "500.00"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.salary, 500.00)

    def test_list_cats(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cat(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SpyCat.objects.count(), 0)
