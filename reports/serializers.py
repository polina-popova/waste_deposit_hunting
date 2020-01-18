from django.conf import settings
from rest_framework import serializers, status

from .models import Report, ContentComplain, State
from .utils import get_location_attrs


class CustomValidationError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request.'
    default_code = 'bad_request'

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = self.default_detail
        else:
            self.detail = detail

        if code is None:
            self.code = self.default_code
        else:
            self.code = code


class CreateReportSerializer(serializers.ModelSerializer):
    waste_deposit = serializers.PrimaryKeyRelatedField(
        source='waste_deposit.id', read_only=True
    )

    class Meta:
        model = Report

        fields = (
            'datetime_received', 'photo', 'lat', 'long', 'comment',
            'feedback_info', 'waste_deposit'
        )

    def validate_latitude(self, lat):
        if not lat:
            raise CustomValidationError(
                detail=settings.NO_LAT_ERROR, code='no_lat'
            )

        if abs(lat) > 90:
            raise CustomValidationError(
                detail=settings.INVALID_LAT_ERROR, code='invalid_lat'
            )

    def validate_longitude(self, long):
        if not long:
            raise CustomValidationError(
                detail=settings.NO_LONG_ERROR, code='no_long'
            )

        if abs(long) > 180:
            raise CustomValidationError(
                detail=settings.INVALID_LONG_ERROR, code='invalid_long'
            )

    def validate_income_photo(self, photo):
        if not photo:
            raise CustomValidationError(
                detail=settings.NO_PHOTO_ERROR, code='no_photo'
            )

    def validate(self, attrs):
        # It is important to validate fields before object-level
        # validation, because of API request in geo state validation
        self.validate_latitude(attrs.get('lat'))
        self.validate_longitude(attrs.get('long'))
        self.validate_income_photo(attrs.get('photo'))

        state, verbose_address = get_location_attrs(attrs['lat'], attrs['long'])

        possible_state = State.objects.only('state_name').filter(state_name__iexact=state)

        if not possible_state:
            settings.LOGGER.info(f'ERROR: invalid_geo_state {state}')

            raise CustomValidationError(
                detail=settings.INVALID_STATE_ERROR, code='invalid_geo_state'
            )
        attrs.update({
            'verbose_address': verbose_address,
            'state': possible_state.first()
        })

        return attrs

    def create(self, validated_data):
        report = super().create(validated_data)

        return report


class ListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report

        fields = ('datetime_received', 'photo', 'lat', 'long', 'id')


class ContentComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentComplain

        fields = ('report', 'body')

    def validate_body(self, body):
        if not body:
            raise CustomValidationError(
                detail=settings.NO_COMPLAIN_BODY_ERROR, code='no_body'
            )
        return body

    def validate(self, attrs):
        self.validate_body(attrs.get('body'))
        return attrs
