from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cat.serializers import SpyCatSerializer
from mission.models import Mission, Target
from cat.models import SpyCat


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = (
            "id",
            "name",
            "country",
            "notes",
            "completed"
        )
        extra_kwargs = {
            "completed": {"read_only": True}
        }

    @staticmethod
    def update_status(target):
        target.completed = not target.completed
        target.save()
        return target


class TargetNoteUpdateSerializer(serializers.Serializer):
    notes = serializers.CharField(max_length=100)

    class Meta:
        fields = ("notes",)

    def update(self, target, validated_data):
        if target.completed or (target.mission and target.mission.completed):
            raise ValidationError(
                "Notes cannot be updated because "
                "the target or mission is completed."
            )

        target.notes = validated_data["notes"]
        target.save()
        return target


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat = serializers.PrimaryKeyRelatedField(
        queryset=SpyCat.objects.all(), write_only=True, required=False
    )
    spy_cat = SpyCatSerializer(source="cat", read_only=True)

    class Meta:
        model = Mission
        fields = (
            "id",
            "cat",
            "spy_cat",
            "completed",
            "targets"
        )
        extra_kwargs = {
            "completed": {"read_only": True},
        }

    def create(self, validated_data):
        cat = validated_data.get("cat")
        if cat and cat.mission and not cat.mission.completed:
            raise serializers.ValidationError(
                f"The cat {cat} already has an active mission."
            )

        targets_data = validated_data.pop("targets")
        if len(targets_data) < 1 or len(targets_data) > 3:
            raise serializers.ValidationError(
                "A mission must have between 1 and 3 targets."
            )

        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission


class MissionSpyCatUpdateSerializer(serializers.Serializer):
    cat_id = serializers.IntegerField(required=False)

    def update_cat(self, mission):
        cat_id = self.validated_data.get("cat_id")

        if cat_id is not None:
            try:
                cat = SpyCat.objects.get(id=cat_id)
            except SpyCat.DoesNotExist:
                raise ValidationError(
                    {"detail": "SpyCat with the given id does not exist."}
                )

            if (
                    hasattr(cat, "mission")
                    and cat.mission and not cat.mission.completed
            ):
                raise ValidationError(
                    f"The cat {cat} already has an active mission."
                )

            mission.cat = cat
        else:
            mission.cat = None

        mission.save()
        return mission
