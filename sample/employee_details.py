"""
@author='bankar'
date = 6/11/2018
"""

class Employee(object):
    def __init__(self,name):
        self.name = name

    def getName(self):
        return self.name



if __name__ == '__main__':
    emp = Employee('rakesh')
    print(emp.getName())