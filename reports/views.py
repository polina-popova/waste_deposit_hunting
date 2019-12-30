from rest_framework import viewsets

from .models import Report
from .serializers import CreateReportSerializer, ListReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()

    def get_serializer_class(self):
        return CreateReportSerializer if self.request.method == 'POST' else ListReportSerializer
