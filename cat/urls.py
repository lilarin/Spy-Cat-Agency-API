from rest_framework.routers import DefaultRouter

from cat.views import SpyCatViewSet

router = DefaultRouter()

router.register("", SpyCatViewSet)


urlpatterns = router.urls

app_name = "cat"
