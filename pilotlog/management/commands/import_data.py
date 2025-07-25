import sys
from django.core.management.base import BaseCommand
from pilotlog.services.importer import PilotLogImporter

class Command(BaseCommand):
    help = 'Imports pilot logbook data from the multi-table JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to import.')

    def handle(self, *args, **options):
        file_path = options['json_file']
        self.stdout.write(self.style.SUCCESS(f'Starting import from {file_path}'))
        try:
            importer = PilotLogImporter(file_path)
            importer.import_all()
            self.stdout.write(self.style.SUCCESS('Import process finished.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Import failed: {e}'))
            sys.exit(1)