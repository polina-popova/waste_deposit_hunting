from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import ReportViewSet


router = routers.SimpleRouter()
router.register(r'reports', ReportViewSet, basename='reports')

urlpatterns = router.urls

urlpatterns.append(path('privacy-policy/', TemplateView.as_view(template_name="privacy_policy.html")),)
