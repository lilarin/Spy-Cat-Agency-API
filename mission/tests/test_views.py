from rest_framework import status
from rest_framework.test import APITestCase
from cat.models import SpyCat
from mission.models import Mission, Target


class MissionViewSetTests(APITestCase):
    def setUp(self):
        self.cat = SpyCat.objects.create(
            name="Agent Whiskers",
            years_of_experience=5,
            breed="Cymric",
            salary="300.00"
        )
        self.mission = Mission.objects.create(cat=self.cat)
        self.mission_url = "/api/mission/"
        self.detail_url = f"{self.mission_url}{self.mission.id}/"

    def test_retrieve_mission(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["spy_cat"]["name"], self.cat.name)

    def test_update_cat_on_mission(self):
        new_cat = SpyCat.objects.create(
            name="Agent Felix",
            years_of_experience=3,
            breed="Maine Coon",
            salary="400.00"
        )
        data = {"cat_id": new_cat.id}
        response = self.client.patch(f"{self.detail_url}update_cat/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mission.refresh_from_db()
        self.assertEqual(self.mission.cat.id, new_cat.id)

    def test_delete_mission_without_cat(self):
        self.mission.cat = None
        self.mission.save()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mission.objects.count(), 0)

    def test_delete_mission_with_cat(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Mission assigned to a cat and cannot be deleted.", response.data["detail"])


class TargetViewSetTests(APITestCase):
    def setUp(self):
        self.cat = SpyCat.objects.create(
            name="Agent Whiskers",
            years_of_experience=5,
            breed="Siberian",
            salary="300.00"
        )
        self.mission = Mission.objects.create(cat=self.cat)
        self.target = Target.objects.create(
            mission=self.mission,
            name="Target 1",
            country="Country A",
            notes="Important mission",
            completed=False
        )
        self.target_detail_url = f"/api/target/{self.target.id}/"

    def test_update_target_status(self):
        response = self.client.patch(f"{self.target_detail_url}update-status/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.target.refresh_from_db()
        self.assertTrue(self.target.completed)

    def test_update_target_notes(self):
        data = {"notes": "Updated mission notes"}
        response = self.client.patch(f"{self.target_detail_url}update-notes/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.target.refresh_from_db()
        self.assertEqual(self.target.notes, "Updated mission notes")

    def test_update_notes_completed_target(self):
        self.target.completed = True
        self.target.save()
        data = {"notes": "Attempt to update notes"}
        response = self.client.patch(f"{self.target_detail_url}update-notes/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
