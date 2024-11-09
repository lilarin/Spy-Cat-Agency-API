from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.response import Response
from rest_framework import viewsets
from cat.models import SpyCat
from cat.serializers import (
    SpyCatSerializer,
    SpyCatSalaryUpdateSerializer,
    SpyCatDetailSerializer
)


@extend_schema(tags=["SpyCats"])
class SpyCatViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = SpyCat.objects.all()

    def get_serializer_class(self):
        if self.action == "partial_update":
            return SpyCatSalaryUpdateSerializer
        elif self.action == "retrieve":
            return SpyCatDetailSerializer
        return SpyCatSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=SpyCatSerializer,
        responses=SpyCatSerializer,
        description="Create a new cat."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        pass

    @extend_schema(
        request=SpyCatSalaryUpdateSerializer,
        responses=SpyCatSerializer,
        description="Update salary for a cat."
    )
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
