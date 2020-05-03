from django.core.management.base import BaseCommand

from reports.models import Report, WasteDeposit
from reports.logic import attach_to_waste_deposit


class Command(BaseCommand):
    help = 'Delete all waste deposit objects and (re)attach all reports.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Reattach all reports.',
        )

    def handle(self, *args, **options):
        if options['all']:
            WasteDeposit.objects.all().delete()

        reports = \
            Report.objects.\
            filter(waste_deposit__isnull=True).\
            order_by('datetime_received')

        if not reports.exists():
            return self.stdout.write('No reports to be attached.')

        for report in reports:
            attach_to_waste_deposit(report)
