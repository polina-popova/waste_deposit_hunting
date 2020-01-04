from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import ReportViewSet


router = routers.SimpleRouter()
router.register(r'reports', ReportViewSet, basename='reports')

urlpatterns = router.urls

urlpatterns += [
    path('privacy-policy/', TemplateView.as_view(template_name="privacy_policy.html")),
    path('customer-agreement/', TemplateView.as_view(template_name="customer_agreement.html")),
]
