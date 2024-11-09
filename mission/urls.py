from rest_framework.routers import DefaultRouter

from mission.views import (
    MissionViewSet,
    TargetViewSet
)

router = DefaultRouter()

router.register("mission", MissionViewSet)
router.register("target", TargetViewSet)

urlpatterns = router.urls

app_name = "mission"
