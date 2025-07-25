import csv
from datetime import timedelta
from typing import Any, Optional
from pilotlog.models import Aircraft, Flight

def format_duration_decimal(duration: Optional[timedelta]) -> float:
    if not duration:
        return 0.0
    return round(duration.total_seconds() / 3600, 2)

class PilotLogExporter:
    """
    Reusable exporter for pilot logbook data to ForeFlight-compatible CSV.
    Usage:
        exporter = PilotLogExporter(csv_path)
        exporter.export_all()
    """
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def export_all(self):
        with open(self.csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            self.export_aircraft(writer)
            self.export_flights(writer)

    def export_aircraft(self, writer: csv.writer):
        writer.writerow(['ForeFlight Logbook Import', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        writer.writerow([])
        writer.writerow(['Aircraft Table', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        aircraft_headers = ['AircraftID', 'EquipmentType', 'TypeCode', 'Year', 'Make', 'Model', 'Category', 'Class', 'GearType', 'EngineType', 'Complex', 'HighPerformance', 'Pressurized', 'TAA']
        writer.writerow(aircraft_headers)
        for aircraft in Aircraft.objects.all().order_by('registration'):
            writer.writerow([
                aircraft.registration,
                '',
                aircraft.model,
                '',
                aircraft.make,
                aircraft.model,
                '', '', '', '',
                'TRUE' if aircraft.complex else 'FALSE',
                'TRUE' if aircraft.high_performance else 'FALSE',
                'TRUE' if getattr(aircraft, 'pressurized', False) else 'FALSE',
                ''
            ])

    def export_flights(self, writer: csv.writer):
        writer.writerow([])
        writer.writerow([])
        writer.writerow(['Flights Table', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        flight_headers = ['Date', 'AircraftID', 'From', 'To', 'Route', 'TimeOut', 'TimeOff', 'TimeOn', 'TimeIn', 'OnDuty', 'OffDuty', 'TotalTime', 'PIC', 'SIC', 'Night', 'Solo', 'CrossCountry', 'NVG']
        writer.writerow(flight_headers)
        flights = Flight.objects.select_related('aircraft', 'departure_airport', 'arrival_airport', 'pilot_in_command', 'second_in_command')
        for flight in flights:
            writer.writerow([
                flight.date.strftime('%Y-%m-%d'),
                flight.aircraft.registration,
                flight.departure_airport.icao_code,
                flight.arrival_airport.icao_code,
                '', '', '', '', '', '', '',
                format_duration_decimal(flight.total_time),
                format_duration_decimal(flight.pic_time),
                format_duration_decimal(flight.sic_time),
                format_duration_decimal(flight.night_time),
                format_duration_decimal(flight.solo_time),
                format_duration_decimal(flight.cross_country_time),
                ''
            ]) 