from django.urls import path
from django.views.generic import TemplateView
from rest_framework_nested import routers

from .views import ReportViewSet, ContentComplainViewSet


reports_router = routers.SimpleRouter()
reports_router.register(r'reports', ReportViewSet, basename='reports')

report_complain_router = routers.NestedSimpleRouter(
    reports_router, r'reports', lookup='report'
)
report_complain_router.register(
    r'content-complain', ContentComplainViewSet, basename='complains'
)

urlpatterns = reports_router.urls + report_complain_router.urls

urlpatterns += [
    path('privacy-policy/', TemplateView.as_view(template_name="privacy_policy.html")),
    path('customer-agreement/', TemplateView.as_view(template_name="customer_agreement.html")),
]
