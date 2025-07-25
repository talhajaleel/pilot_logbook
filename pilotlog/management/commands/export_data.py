import sys
from django.core.management.base import BaseCommand
from pilotlog.services.exporter import PilotLogExporter

class Command(BaseCommand):
    help = 'Exports logbook data to a ForeFlight-compatible CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path for the output CSV file.')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        self.stdout.write(self.style.SUCCESS(f'Exporting data to {file_path}'))
        try:
            exporter = PilotLogExporter(file_path)
            exporter.export_all()
            self.stdout.write(self.style.SUCCESS('Successfully exported data.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Export failed: {e}'))
            sys.exit(1)