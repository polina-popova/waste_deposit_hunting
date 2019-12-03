from rest_framework import routers

from .views import ReportViewSet


router = routers.SimpleRouter()
router.register(r'reports', ReportViewSet, basename='reports')

urlpatterns = router.urls
