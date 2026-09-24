class HRManagementSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee_id, employee_details):
        if employee_id in self.employees:
            return False
        employee_details["employee_id"] = employee_id
        self.employees[employee_id] = employee_details
        return True

    def remove_employee(self, employee_id):
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        return False

    def update_employee(self, employee_id, update_details):
        if employee_id not in self.employees:
            return False
        for field in update_details:
            if field not in self.employees[employee_id]:
                return False
        self.employees[employee_id].update(update_details)
        return True

    def get_employee(self, employee_id):
        if employee_id in self.employees:
            return self.employees[employee_id]
        return False

    def list_employees(self):
        return self.employees

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
