from ..models.employee import Employee

def CreateNewEmployee(name):
    user = Employee()
    user.name = name
    user.save()
    return user

def GetEmployeeByName(name):
    try:
        employee = Employee.objects.get({'name': str(name)})
        return employee
    except:
        return None