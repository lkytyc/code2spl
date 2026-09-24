class HRManagementSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee_id, name, position, department, salary):
        if employee_id in self.employees:
            return False
        self.employees[employee_id] = {
            "name": name,
            "position": position,
            "department": department,
            "salary": salary,
        }
        return True

    def remove_employee(self, employee_id):
        if employee_id not in self.employees:
            return False
        del self.employees[employee_id]
        return True

    def update_employee(self, employee_id, employee_info):
        employee = self.get_employee(employee_id)
        if not employee:
            return False
        for key in employee_info:
            if key not in employee:
                return False
        employee.update(employee_info)
        return True

    def get_employee(self, employee_id):
        if employee_id in self.employees:
            return self.employees[employee_id]
        return False

    def list_employees(self):
        employee_list = {}
        for employee_id, employee_data in self.employees.items():
            employee_list[employee_id] = {
                "employee_ID": employee_id,
                **employee_data,
            }
        return employee_list

import unittest

class HRManagementSystemTestRemoveEmployee(unittest.TestCase):
    def test_remove_employee(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.remove_employee(1), True)
        self.assertEqual(hr_system.employees, {})

    def test_remove_employee_2(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.remove_employee(1), True)
        self.assertEqual(hr_system.remove_employee(1), False)
        self.assertEqual(hr_system.employees, {})

    def test_remove_employee_3(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}, 2: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.remove_employee(1), True)
        self.assertEqual(hr_system.employees, {2: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}})

    def test_remove_employee_4(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}, 2: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.remove_employee(1), True)
        self.assertEqual(hr_system.remove_employee(2), True)
        self.assertEqual(hr_system.employees, {})

    def test_remove_employee_5(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}, 2: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.remove_employee(1), True)
        self.assertEqual(hr_system.remove_employee(2), True)
        self.assertEqual(hr_system.remove_employee(1), False)
        self.assertEqual(hr_system.remove_employee(2), False)
        self.assertEqual(hr_system.employees, {})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
