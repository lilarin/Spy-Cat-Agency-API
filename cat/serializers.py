import requests
from rest_framework import serializers
from cat.models import SpyCat


class SpyCatSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_breed(value):
        try:
            response = requests.get("https://api.thecatapi.com/v1/breeds")
            response.raise_for_status()
            breeds_data = response.json()
        except requests.exceptions.RequestException as error:
            raise serializers.ValidationError(f"Error fetching breed data: {str(error)}")
        valid_breeds = {breed["name"] for breed in breeds_data}
        for breed in breeds_data:
            if "alt_names" in breed and breed["alt_names"]:
                alt_names = [name.strip() for name in breed["alt_names"].split(",")]
                valid_breeds.update(alt_names)
        if value not in valid_breeds:
            raise serializers.ValidationError("Invalid breed name.")
        return value

    class Meta:
        model = SpyCat
        fields = (
            "id",
            "name",
            "years_of_experience",
            "breed",
            "salary"
        )


class SpyCatDetailSerializer(SpyCatSerializer):
    class Meta:
        model = SpyCat
        fields = (
            "name",
            "years_of_experience",
            "breed",
            "salary"
        )


class SpyCatSalaryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = (
            "salary",
        )
