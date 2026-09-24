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
            "salary": salary
        }
        return True

    def remove_employee(self, employee_id):
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        return False

    def get_employee(self, employee_id):
        if employee_id in self.employees:
            return self.employees[employee_id]
        return False

    def update_employee(self, employee_id, employee_info):
        employee = self.get_employee(employee_id)
        if employee is False:
            return False

        for key in employee_info:
            if key not in employee:
                return False

        for key, value in employee_info.items():
            employee[key] = value
        return True

    def list_employees(self):
        all_employees = {}
        for employee_id, employee_data in self.employees.items():
            employee_record = dict(employee_data)
            employee_record["employee_ID"] = employee_id
            all_employees[employee_id] = employee_record
        return all_employees

import unittest

class HRManagementSystemTestGetEmployee(unittest.TestCase):
    def test_get_employee(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.get_employee(1), {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000})

    def test_get_employee_2(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {}
        self.assertEqual(hr_system.get_employee(1), False)

    def test_get_employee_3(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.get_employee(2), False)

    def test_get_employee_4(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.get_employee(1), {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000})
        self.assertEqual(hr_system.get_employee(1), {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000})

    def test_get_employee_5(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}, 2: {'name': 'Jane', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.get_employee(1), {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000})
        self.assertEqual(hr_system.get_employee(2), {'name': 'Jane', 'position': 'Manager', 'department': 'Sales', 'salary': 100000})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
