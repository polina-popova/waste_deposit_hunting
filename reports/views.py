from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from .models import Report, ContentComplain
from .serializers import CreateReportSerializer, ListReportSerializer, \
    ContentComplainSerializer


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


class ContentComplainViewSet(viewsets.GenericViewSet):
    queryset = ContentComplain.objects.all()
    serializer_class = ContentComplainSerializer
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        report_pk = kwargs.get('report_pk')
        generics.get_object_or_404(Report.objects.all(), pk=report_pk)

        data = {
            'report': report_pk,
            'body': request.data.get('body')
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)