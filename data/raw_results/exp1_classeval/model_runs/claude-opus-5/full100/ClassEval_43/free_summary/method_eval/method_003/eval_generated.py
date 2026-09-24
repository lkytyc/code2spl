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

    def get_employee(self, employee_id):
        if employee_id not in self.employees:
            return False
        return self.employees[employee_id]

    def update_employee(self, employee_id, updates):
        employee = self.get_employee(employee_id)
        if employee is False:
            return False
        for key in updates:
            if key not in employee:
                return False
        for key, value in updates.items():
            employee[key] = value
        return True

    def list_employees(self):
        if not self.employees:
            return {}
        result = {}
        for employee_id, data in self.employees.items():
            entry = dict(data)
            entry["employee_ID"] = employee_id
            result[employee_id] = entry
        return result

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
