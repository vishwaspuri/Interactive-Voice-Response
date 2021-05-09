from .employee import Employee

def CreateNewEmployee(name):
    user = Employee()
    user.name = str(name).lower()
    user.save()
    return user

def GetEmployeeByName(name) -> Employee:
    employee = Employee.objects(name=str(name).lower()).first()
    return employee