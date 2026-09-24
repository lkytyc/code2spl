class HRManagementSystem:
    """
    This is a class as personnel management system that implements functions such as adding, deleting, querying, and updating employees
    """

    def __init__(self):
        """
        Initialize the HRManagementSystem withan attribute employees, which is an empty dictionary.
        """
        self.employees = {}

    def add_employee(self, employee_id, name, position, department, salary):
        """
        Add a new employee to the HRManagementSystem.
        """
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
        """
        Remove an employee from the HRManagementSystem.
        """
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        return False

    def update_employee(self, employee_id: int, employee_info: dict):
        """
        Update an employee's information in the HRManagementSystem.
        """
        employee = self.get_employee(employee_id)

        if employee is False:
            return False

        for key, value in employee_info.items():
            if key not in employee:
                return False

        for key, value in employee_info.items():
            employee[key] = value

        return True

    def get_employee(self, employee_id):
        """
        Get an employee's information from the HRManagementSystem.
        """
        if employee_id in self.employees:
            return self.employees[employee_id]
        return False

    def list_employees(self):
        """
        List all employees' information in the HRManagementSystem.
        """
        employee_data = {}

        if self.employees:
            for employee_id, employee_info in self.employees.items():
                employee_details = {}
                employee_details["employee_ID"] = employee_id

                for key, value in employee_info.items():
                    employee_details[key] = value

                employee_data[employee_id] = employee_details

        return employee_data

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
