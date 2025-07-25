import json
import ast
from datetime import timedelta
from typing import Any, Dict, List
from pilotlog.models import Aircraft, Airport, Person, Flight
from django.db import transaction

class PilotLogImporter:
    """
    Reusable importer for pilot logbook data from JSON.
    Usage:
        importer = PilotLogImporter(json_path)
        importer.import_all()
    """
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data = self._load_json()
        self.records = {"Aircraft": [], "Flight": [], "Airport": [], "People": []}
        self._split_records()

    def _load_json(self) -> list:
        with open(self.json_path, 'r', encoding='utf-8-sig') as f:
            raw_content = f.read().strip()

        try:
            # Step 1: Convert the escaped string to a proper string (removes \")
            unescaped = ast.literal_eval(f"'''{raw_content}'''")
            # Step 2: Parse the result as JSON
            data = json.loads(unescaped)
            return data
        except Exception as e:
            raise Exception(f"Import failed: Could not decode JSON content. Error: {e}")

    def _split_records(self):
        for entry in self.data:
            table_name = entry.get("table")
            if table_name in self.records:
                self.records[table_name].append(entry)

    @transaction.atomic
    def import_all(self):
        self.import_aircraft(self.records["Aircraft"])
        self.import_airports(self.records["Airport"])
        self.import_people(self.records["People"])
        self.import_flights(self.records["Flight"])

    def import_aircraft(self, aircraft_data: List[Dict[str, Any]]):
        for entry in aircraft_data:
            meta = entry.get('meta', {})
            Aircraft.objects.update_or_create(
                guid=entry['guid'],
                defaults={
                    'registration': meta.get('Reference'),
                    'make': meta.get('Make'),
                    'model': meta.get('Model'),
                    'complex': meta.get('Complex', False),
                    'high_performance': meta.get('HighPerf', False),
                    'tailwheel': meta.get('Tailwheel', False),
                    'aerobatic': meta.get('Aerobatic', False),
                    'source_modified_timestamp': entry.get('_modified')
                }
            )

    def import_airports(self, airport_data: List[Dict[str, Any]]):
        for entry in airport_data:
            meta = entry.get('meta', {})
            Airport.objects.update_or_create(
                guid=entry['guid'],
                defaults={
                    'icao_code': meta.get('ICAO'),
                    'name': meta.get('Name', ''),
                }
            )

    def import_people(self, people_data: List[Dict[str, Any]]):
        for entry in people_data:
            meta = entry.get('meta', {})
            Person.objects.update_or_create(
                guid=entry['guid'],
                defaults={
                    'full_name': meta.get('Name'),
                }
            )

    def import_flights(self, flight_data: List[Dict[str, Any]]):
        for entry in flight_data:
            meta = entry.get('meta', {})
            try:
                aircraft = Aircraft.objects.get(guid=meta['AircraftGUID'])
                departure_airport = Airport.objects.get(guid=meta['DepartureAirportGUID'])
                arrival_airport = Airport.objects.get(guid=meta['ArrivalAirportGUID'])
                pic = Person.objects.filter(guid=meta.get('PICGUID')).first()
                sic = Person.objects.filter(guid=meta.get('SICGUID')).first()
            except Exception:
                continue
            Flight.objects.update_or_create(
                guid=entry['guid'],
                defaults={
                    'date': meta.get('Date'),
                    'aircraft': aircraft,
                    'departure_airport': departure_airport,
                    'arrival_airport': arrival_airport,
                    'pilot_in_command': pic,
                    'second_in_command': sic,
                    'total_time': self.parse_duration(meta.get('TotalTime')),
                    'pic_time': self.parse_duration(meta.get('PICTime')),
                    'sic_time': self.parse_duration(meta.get('SICTime')),
                    'night_time': self.parse_duration(meta.get('NightTime')),
                    'solo_time': self.parse_duration(meta.get('SoloTime')),
                    'cross_country_time': self.parse_duration(meta.get('CrossCountryTime')),
                    'remarks': meta.get('Remarks', ''),
                    'source_modified_timestamp': entry.get('_modified')
                }
            )

    @staticmethod
    def parse_duration(time_value: Any) -> timedelta:
        if isinstance(time_value, (int, float)):
            return timedelta(minutes=time_value)
        return timedelta() 