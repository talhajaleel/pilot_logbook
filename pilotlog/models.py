# pilotlog/models.py
import uuid
from django.db import models
from datetime import timedelta

# This model is much more detailed now.
class Aircraft(models.Model):
    # We will use the 'guid' from the JSON as a reliable, unique identifier.
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration = models.CharField(max_length=10, unique=True, db_index=True) # From meta.Reference
    make = models.CharField(max_length=50, blank=True) # From meta.Make
    model = models.CharField(max_length=50, blank=True) # From meta.Model

    # Boolean flags from meta and for CSV export
    complex = models.BooleanField(default=False)
    high_performance = models.BooleanField(default=False)
    tailwheel = models.BooleanField(default=False)
    aerobatic = models.BooleanField(default=False)
    pressurized = models.BooleanField(default=False) # Not in JSON, but needed for CSV
    
    # We store the last modification timestamp from the source data
    source_modified_timestamp = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.registration

class Airport(models.Model):
    # This model remains largely the same, but let's assume it's also in the JSON
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    icao_code = models.CharField(max_length=4, unique=True, db_index=True)
    name = models.CharField(max_length=100, blank=True)
    # other fields like latitude, longitude, etc. could be added

    def __str__(self):
        return self.icao_code

class Person(models.Model):
    # Also likely has a GUID in the full JSON
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.full_name

class Flight(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(db_index=True)

    # ForeignKeys link to our normalized tables
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT, related_name="flights")
    departure_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="departures")
    arrival_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="arrivals")

    # The people involved
    pilot_in_command = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="flights_as_pic", null=True, blank=True)
    second_in_command = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="flights_as_sic", null=True, blank=True)

    # Time fields. DurationField is perfect for this. We will parse the source data into timedeltas.
    # The CSV asks for Decimal for some, so we will convert on export.
    total_time = models.DurationField(default=timedelta)
    sic_time = models.DurationField(default=timedelta)
    pic_time = models.DurationField(default=timedelta)
    night_time = models.DurationField(default=timedelta)
    solo_time = models.DurationField(default=timedelta)
    cross_country_time = models.DurationField(default=timedelta)
    
    remarks = models.TextField(blank=True)
    source_modified_timestamp = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-date']