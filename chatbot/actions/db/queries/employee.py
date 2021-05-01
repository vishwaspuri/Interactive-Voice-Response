from models.employee import Employee

def CreateNewEmployee(name):
    user = Employee()
    user.name = name
    user.save()
    return user

def GetEmployeeByName(name):
    employee = Employee.objects.get({'name': name})
    return employee