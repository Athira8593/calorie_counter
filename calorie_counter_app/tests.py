from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import FoodItem, FoodItemLabel


class FoodItemListAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="creator", password="pass12345")
        self.url = reverse("list-fooditems")

    def test_list_fooditems_returns_only_admin_approved_items(self):
        label = FoodItemLabel.objects.create(name="Protein")

        approved_item = FoodItem.objects.create(
            name="Paneer",
            calories=265,
            created=self.user,
            approved_by_admin=True,
        )
        approved_item.labels.add(label)

        not_approved_item = FoodItem.objects.create(
            name="Secret Recipe",
            calories=500,
            created=self.user,
            approved_by_admin=False,
        )
        not_approved_item.labels.add(label)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], approved_item.id)
        self.assertEqual(response.data[0]["name"], approved_item.name)

    def test_list_fooditems_response_contains_expected_serializer_fields(self):
        label1 = FoodItemLabel.objects.create(name="Vegan")
        label2 = FoodItemLabel.objects.create(name="Low-Carb")
        food_item = FoodItem.objects.create(
            name="Tofu Salad",
            calories=180,
            created=self.user,
            approved_by_admin=True,
        )
        food_item.labels.add(label1, label2)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        item = response.data[0]
        self.assertSetEqual(set(item.keys()), {"id", "name", "calories", "labels"})
        self.assertEqual(item["id"], food_item.id)
        self.assertEqual(item["name"], "Tofu Salad")
        self.assertEqual(item["calories"], 180)
        self.assertCountEqual(item["labels"], [label1.id, label2.id])
