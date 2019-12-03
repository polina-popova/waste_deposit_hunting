from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer

from .models import Report, WasteDeposit


class ReportSerializer(GeoModelSerializer):
    waste_deposit = serializers.PrimaryKeyRelatedField(
        source='waste_deposit.id', read_only=True
    )

    class Meta:
        model = Report
        geo_field = 'location'

        fields = (
            'datetime_received', 'photo', 'location', 'comment',
            'feedback_info', 'waste_deposit'
        )

    def create(self, validated_data):
        waste_deposit = WasteDeposit.objects.create(location=validated_data['location'])
        validated_data['waste_deposit'] = waste_deposit

        return super().create(validated_data)
