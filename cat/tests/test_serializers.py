from unittest.mock import patch
from rest_framework.test import APITestCase
from cat.models import SpyCat
from cat.serializers import SpyCatSerializer, SpyCatSalaryUpdateSerializer

class SpyCatSerializerTests(APITestCase):
    def setUp(self):
        self.cat_data = {
            "name": "Whiskers",
            "years_of_experience": 5,
            "breed": "Cymric",
            "salary": "300.00"
        }

    @patch("requests.get")
    def test_validate_breed_valid(self, mock_get):
        mock_get.return_value.json.return_value = [{"name": "Cymric"}]
        mock_get.return_value.status_code = 200

        serializer = SpyCatSerializer(data=self.cat_data)
        self.assertTrue(serializer.is_valid())

    @patch("requests.get")
    def test_validate_breed_invalid(self, mock_get):
        mock_get.return_value.json.return_value = [{"name": "Maine Coon"}]
        mock_get.return_value.status_code = 200

        serializer = SpyCatSerializer(data=self.cat_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("breed", serializer.errors)
        self.assertEqual(
            serializer.errors["breed"][0],
            "Invalid breed name."
        )

    def test_salary_update_serializer(self):
        spy_cat = SpyCat.objects.create(**self.cat_data)
        data = {"salary": "500.00"}
        serializer = SpyCatSalaryUpdateSerializer(instance=spy_cat, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        spy_cat.refresh_from_db()
        self.assertEqual(spy_cat.salary, 500.00)
