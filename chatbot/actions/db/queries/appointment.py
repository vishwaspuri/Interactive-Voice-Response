from models.appointment import Appointment

def CreateNewAppointment(employee, customer_name, appointment_time):
    appointment = Appointment()
    appointment.customer_name = customer_name
    appointment.time = appointment_time
    appointment.employee = employee
    appointment.save()