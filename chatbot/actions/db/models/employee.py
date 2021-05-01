from pymodm import MongoModel, fields
from pymongo.read_preferences import ReadPreference


class Employee(MongoModel):
    name = fields.CharField()

    class Meta:
        # Read from secondaries.
        read_preference = ReadPreference.SECONDARY