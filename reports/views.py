from rest_framework import viewsets
from rest_framework.response import Response

from .models import Report
from .serializers import CreateReportSerializer, ListReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    http_method_names = ['post', 'get']

    def get_serializer_class(self):
        return CreateReportSerializer if self.request.method == 'POST' else ListReportSerializer

    def list(self, request, *args, **kwargs):
        # Do not use pagination if query params is 'all=true'
        if request.query_params.get('all') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(data={'results': serializer.data})

        return super().list(request, *args, **kwargs)
