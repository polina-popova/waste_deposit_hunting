from rest_framework import serializers

from .models import Report, WasteDeposit


class ReportSerializer(serializers.ModelSerializer):
    waste_deposit = serializers.PrimaryKeyRelatedField(
        source='waste_deposit.id', read_only=True
    )

    class Meta:
        model = Report

        fields = (
            'datetime_received', 'photo', 'lat', 'long', 'comment',
            'feedback_info', 'waste_deposit'
        )

    def create(self, validated_data):
        waste_deposit = WasteDeposit.objects.create(
            lat=validated_data['lat'], long=validated_data['long']
        )
        validated_data['waste_deposit'] = waste_deposit

        return super().create(validated_data)
