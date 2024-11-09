from rest_framework import (
    viewsets,
    status
)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin
)
from drf_spectacular.utils import extend_schema

from mission.models import (
    Mission,
    Target
)
from mission.serializers import (
    MissionSerializer,
    TargetSerializer,
    MissionSpyCatUpdateSerializer,
    TargetNoteUpdateSerializer
)


@extend_schema(tags=["Missions"])
class MissionViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @extend_schema(
        request=MissionSerializer,
        responses=MissionSerializer,
        description="Create a mission with associated targets."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=MissionSerializer,
        description="Retrieve a list of all missions."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses=MissionSerializer,
        description="Retrieve a single mission by ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Delete a mission if not assigned to a cat."
    )
    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response(
                {"detail": "Mission assigned to a cat and cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        request=MissionSpyCatUpdateSerializer,
        responses=MissionSerializer
    )
    @action(detail=True, methods=["patch"])
    def update_cat(self, request, *args, **kwargs):
        mission = self.get_object()
        serializer = MissionSpyCatUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_mission = serializer.update_cat(mission)
        return Response(
            MissionSerializer(updated_mission).data, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Targets"])
class TargetViewSet(viewsets.GenericViewSet):
    queryset = Target.objects.all()

    def get_serializer_class(self):
        if self.action == "update_notes":
            return TargetNoteUpdateSerializer
        elif self.action == "update_status":
            return TargetSerializer
        return TargetSerializer

    @extend_schema(
        responses=TargetSerializer,
        description="Retrieve a single target and update its status."
    )
    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_status(self, request, pk):
        try:
            target = self.get_object()
            serializer = self.get_serializer(target)
            updated_target = serializer.update_status(target)

            updated_serializer = TargetSerializer(updated_target)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        except Target.DoesNotExist:
            return Response(
                {"error": "Target with specified ID not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        request=TargetNoteUpdateSerializer,
        responses=TargetSerializer,
        description="Update the notes of a target if it is not completed yet."
    )
    @action(detail=True, methods=["patch"], url_path="update-notes")
    def update_notes(self, request, pk):
        target = self.get_object()

        serializer = self.get_serializer(target, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_target = serializer.save()

        return Response(
            TargetSerializer(updated_target).data, status=status.HTTP_200_OK
        )
