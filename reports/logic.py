from django.conf import settings
from geopy.distance import geodesic

from reports.models import WasteDeposit, Report


def attach_to_waste_deposit(report: Report) -> None:
    """
    Try to find an existing waste deposit in 5 meters from the new report location
    to attach report. If close waste deposit does not exist
    the new one with report`s coordinates will be created.
    """

    waste_deposits = WasteDeposit.objects.all()

    close_waste_deposit = None

    for waste_deposit in waste_deposits:
        distance = geodesic(report.location, waste_deposit.location).meters
        if distance <= settings.WASTE_DEPOSIT_DISTANCE_IN_METERS:
            settings.LOGGER.info(
                f'Attaching report {report.id} to the existing '
                f'waste deposit {waste_deposit.id} in {round(distance, ndigits=2)} '
                f'meters.'
            )
            close_waste_deposit = waste_deposit
            break

    if not close_waste_deposit:
        settings.LOGGER.info(
            f'Creating new waste deposit for the report {report.id}.'
        )
        close_waste_deposit = WasteDeposit.objects.create(
            lat=report.lat, long=report.long
        )

    report.waste_deposit_id = close_waste_deposit
    report.save()
