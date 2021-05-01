from pymongo.read_preferences import ReadPreference
from models.employee import Employee
from pymodm import MongoModel, fields

class Appointment(MongoModel):
    customer_name = fields.CharField(required=True)
    time = fields.DateTimeField(required=True)
    employee = fields.ReferenceField(Employee, required=True)

    class Meta:
        # Read from secondaries.
        read_preference = ReadPreference.SECONDARY