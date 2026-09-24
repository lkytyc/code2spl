class HRManagementSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee_id, name, position, department, salary):
        employee_exists = employee_id in self.employees
        if employee_exists:
            return False
        self.employees[employee_id] = {
            "name": name,
            "position": position,
            "department": department,
            "salary": salary,
        }
        return True

    def get_employee(self, employee_id):
        employee_exists = employee_id in self.employees
        if employee_exists:
            return self.employees[employee_id]
        return False

    def list_employees(self):
        employee_data = {}
        if self.employees:
            for employee_id, employee_info in self.employees.items():
                employee_details = {}
                employee_details["employee_ID"] = employee_id
                for key, value in employee_info.items():
                    employee_details[key] = value
                employee_data[employee_id] = employee_details
        return employee_data

    def remove_employee(self, employee_id):
        employee_exists = employee_id in self.employees
        if employee_exists:
            del self.employees[employee_id]
            return True
        return False

    def update_employee(self, employee_id, employee_info):
        employee = self.get_employee(employee_id)
        employee_is_false = employee is False
        if employee_is_false:
            return False
        for key, value in employee_info.items():
            if key not in employee:
                return False
        for key, value in employee_info.items():
            employee[key] = value
        return True

import unittest

class HRManagementSystemTestUpdateEmployee(unittest.TestCase):
    def test_update_employee(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.update_employee(1, {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000}), True)
        self.assertEqual(hr_system.employees[1], {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000})

    def test_update_employee_2(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {}
        self.assertEqual(hr_system.update_employee(1, {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000}), False)
        self.assertEqual(hr_system.employees, {})

    def test_update_employee_3(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.update_employee(2, {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000}), False)
        self.assertEqual(hr_system.employees, {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}})

    def test_update_employee_4(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.update_employee(1, {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000}), True)
        self.assertEqual(hr_system.update_employee(1, {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000}), True)
        self.assertEqual(hr_system.employees[1], {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000})

    def test_update_employee_5(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.update_employee(1, {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000}), True)
        self.assertEqual(hr_system.update_employee(1, {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000}), True)
        self.assertEqual(hr_system.update_employee(1, {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}), True)
        self.assertEqual(hr_system.employees[1], {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000})

    def test_update_employee_6(self):
        hr_system = HRManagementSystem()
        hr_system.employees = {1: {'name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 100000}}
        self.assertEqual(hr_system.update_employee(1, {'Name': 'John', 'position': 'Manager', 'department': 'Sales', 'salary': 20000}), False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
