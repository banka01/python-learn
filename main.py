"""
@author='bankar'
date = 6/11/2018
"""


from sample.employee_details import Employee

emp = Employee('banka')
print(emp.getName())

class AA:

    def __getattr__(self, item):

        self.__dict__[item] = 'welcom'



a= AA()
b=AA()
print(a.test)
print(a.test)