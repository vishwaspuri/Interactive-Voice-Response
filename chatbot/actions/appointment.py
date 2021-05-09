from mongoengine import Document, StringField, DateTimeField
from mongoengine.fields import ReferenceField
from .employee import Employee

class Appointment(Document):
    customer_name = StringField(required=True)
    time = DateTimeField(required=True)
    employee = ReferenceField(Employee, required=True)

    def to_dict(self):
        return {
            '_id': str(self.id),
            'customer_name': self.customer_name,
            'employee': self.employee.to_dict(),
            'appointment_time': self.appointment
        }