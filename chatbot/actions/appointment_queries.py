from .appointment import Appointment

def CreateNewAppointment(employee, customer_name, appointment_time):
    appointment = Appointment()
    appointment.customer_name = str(customer_name).lower()
    appointment.time = appointment_time
    appointment.employee = employee
    appointment.save()

def GetAppointment(employee, customer_name, appointment_time):
    try:
        app = Appointment.objects(employee = employee, customer_name=customer_name, time=customer_name).first()
        return app
    except:
        return None

def CancelAppointment(employee, customer_name, appointment_time):
    app = Appointment.objects(employee = employee, customer_name=customer_name, time=customer_name).first()
    if app is not None:
        try:
            app.delete()
            return True
        except:
            return False
    else:
        return False