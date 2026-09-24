class HRManagementSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee_id, name, position, department, salary):
        if employee_id in self.employees:
            return False
        self.employees[employee_id] = {
            'name': name,
            'position': position,
            'department': department,
            'salary': salary
        }
        return True

    def remove_employee(self, employee_id):
        if employee_id not in self.employees:
            return False
        del self.employees[employee_id]
        return True

    def update_employee(self, employee_id, updates):
        if employee_id not in self.employees:
            return False
        valid_fields = {'name', 'position', 'department', 'salary'}
        if not set(updates.keys()).issubset(valid_fields):
            return False
        self.employees[employee_id].update(updates)
        return True

    def get_employee(self, employee_id):
        if employee_id not in self.employees:
            return False
        return self.employees[employee_id]

    def list_employees(self):
        result = {}
        for emp_id, data in self.employees.items():
            result[emp_id] = {'employee_id': emp_id, **data}
        return result

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
