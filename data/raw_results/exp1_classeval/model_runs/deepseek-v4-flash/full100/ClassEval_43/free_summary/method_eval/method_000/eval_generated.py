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

class HRManagementSystemTestAddEmployee(unittest.TestCase):
    def test_add_employee(self):
        hr_system = HRManagementSystem()
        self.assertEqual(hr_system.add_employee(1, "John Doe", "Manager", "HR", 5000), True)
        self.assertEqual(hr_system.employees[1], {'name': 'John Doe', 'position': 'Manager', 'department': 'HR', 'salary': 5000})

    def test_add_employee_2(self):
        hr_system = HRManagementSystem()
        self.assertEqual(hr_system.add_employee(1, "John Doe", "Manager", "HR", 5000), True)
        self.assertEqual(hr_system.add_employee(1, "John Doe", "Manager", "HR", 5000), False)
        self.assertEqual(hr_system.employees[1], {'name': 'John Doe', 'position': 'Manager', 'department': 'HR', 'salary': 5000})

    def test_add_employee_3(self):
        hr_system = HRManagementSystem()
        self.assertEqual(hr_system.add_employee(1, "John Doe", "Manager", "HR", 5000), True)
        self.assertEqual(hr_system.add_employee(2, "John Doe", "Manager", "HR", 5000), True)
        self.assertEqual(hr_system.employees,{1: {'name': 'John Doe', 'position': 'Manager', 'department': 'HR', 'salary': 5000}, 2: {'name': 'John Doe', 'position': 'Manager', 'department': 'HR', 'salary': 5000}})

    def test_add_employee_4(self):
        hr_system = HRManagementSystem()
        self.assertEqual(hr_system.add_employee(1, "John Doe", "Manager", "HR", 5000), True)
        self.assertEqual(hr_system.add_employee(2, "John Doe", "Manager", "HR", 5000), True)
        self.assertEqual(hr_system.add_employee(1, "John Doe", "Manager", "HR", 5000), False)
        self.assertEqual(hr_system.employees,{1: {'name': 'John Doe', 'position': 'Manager', 'department': 'HR', 'salary': 5000}, 2: {'name': 'John Doe', 'position': 'Manager', 'department': 'HR', 'salary': 5000}})

    def test_add_employee_5(self):
        hr_system = HRManagementSystem()
        self.assertEqual(hr_system.add_employee(1, "John Doe", "Manager", "HR", 5000), True)
        self.assertEqual(hr_system.add_employee(2, "John Doe", "Manager", "HR", 5000), True)
        self.assertEqual(hr_system.add_employee(1, "John Doe", "Manager", "HR", 5000), False)
        self.assertEqual(hr_system.add_employee(2, "John Doe", "Manager", "HR", 5000), False)
        self.assertEqual(hr_system.employees,{1: {'name': 'John Doe', 'position': 'Manager', 'department': 'HR', 'salary': 5000}, 2: {'name': 'John Doe', 'position': 'Manager', 'department': 'HR', 'salary': 5000}})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
