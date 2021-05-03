from ..models.employee import Employee

def CreateNewEmployee(name):
    user = Employee()
    user.name = str(name).to_lower()
    user.save()
    return user

def GetEmployeeByName(name):
    try:
        employee = Employee.objects.get({'name': str(name).to_lower()})
        return employee
    except:
        return None