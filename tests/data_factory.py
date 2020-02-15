import factory
from factory.django import DjangoModelFactory
from django.conf import settings

from reports.models import Report, State, WasteDeposit


class PhotoProvider:
    pass


class WasteDepositFactory(DjangoModelFactory):
    class Meta:
        model = WasteDeposit

    lat = factory.Faker('latitude')
    long = factory.Faker('longitude')


class StateFactory(DjangoModelFactory):
    class Meta:
        model = State

    state_name = factory.Iterator(
        [
            'Архангельская область', 'Автономная ресублика Абхазия',
            'Вологодская область'
        ]
    )
    emails = factory.Iterator(['["arkhangelsk@mail.ru"]', '["abhasia@mail.ru"]', ''])
    is_draft = False


class ValidReportFactory(DjangoModelFactory):
    class Meta:
        model = Report

    lat = factory.Iterator([64.61833411, 42.707734971858926])
    long = factory.Iterator([40.9587337, 41.47001143544912])
    photo = factory.django.ImageField(color='blue')
    state = factory.SubFactory(StateFactory)
    waste_deposit = factory.SubFactory(WasteDepositFactory)
