import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main_testable import initialize_database, add_employee, get_all_employees, delete_employee, update_employee_field


class TestEmployeeApp(unittest.TestCase):
    def setUp(self):
        """Инициализация тестовой базы данных перед каждым тестом."""
        initialize_database()

    def tearDown(self):
        """Очистка базы данных после каждого теста."""
        db_path = os.path.join(os.path.dirname(__file__), "../employees.db")
        if os.path.exists(db_path):
            os.remove(db_path)


    def test_view_employees_empty(self):
        """Тест отображения сотрудников при пустой базе данных."""
        employees = get_all_employees()
        self.assertEqual(len(employees), 0)

    def test_add_employee(self):
        """Тест добавления сотрудника с корректными данными."""
        add_employee("Максим", "Воронов", "max.voronov@mail.com", "25.05.1999", 60000.75)
        employees = get_all_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0][1], "Максим")
        self.assertEqual(employees[0][2], "Воронов")
        self.assertEqual(employees[0][3], "max.voronov@mail.com")
        self.assertEqual(employees[0][4], "1999-05-25")
        self.assertEqual(employees[0][5], 60000.75)

    def test_update_all_fields(self):
        """Тест обновления всех данных сотрудника."""
        add_employee("Антон", "Савчук", "anton@mail.com", "01.01.1990", 50000)
        employees = get_all_employees()
        emp_id = employees[0][0]
        update_employee_field(emp_id, "first_name", "Алексей")
        update_employee_field(emp_id, "last_name", "Смирнов")
        update_employee_field(emp_id, "email", "alexey.smirnov@mail.com")
        update_employee_field(emp_id, "birth_date", "01.01.1992")
        update_employee_field(emp_id, "salary", 75000.50)
        employees = get_all_employees()
        self.assertEqual(employees[0][1], "Алексей")
        self.assertEqual(employees[0][2], "Смирнов")
        self.assertEqual(employees[0][3], "alexey.smirnov@mail.com")
        self.assertEqual(employees[0][4], "01.01.1992")
        self.assertEqual(employees[0][5], 75000.50)

    def test_update_specific_field(self):
        """Тест обновления отдельного поля сотрудника."""
        add_employee("Антон", "Савчук", "anton@mail.com", "01.01.1990", 50000)
        employees = get_all_employees()
        emp_id = employees[0][0]
        update_employee_field(emp_id, "first_name", "Алексей")
        employees = get_all_employees()
        self.assertEqual(employees[0][1], "Алексей")
        self.assertEqual(employees[0][2], "Савчук")

    def test_delete_employee(self):
        """Тест удаления сотрудника."""
        add_employee("Антон", "Савчук", "anton@mail.com", "01.01.1990", 50000)
        employees = get_all_employees()
        self.assertEqual(len(employees), 1)
        emp_id = employees[0][0]
        delete_employee(emp_id)
        employees = get_all_employees()
        self.assertEqual(len(employees), 0)

    def test_invalid_email(self):
        """Тест добавления сотрудника с некорректным email."""
        with self.assertRaises(ValueError):
            add_employee("Антон", "Савчук", "antonmail.com", "01.01.1990", 50000)

    def test_invalid_date(self):
        """Тест добавления сотрудника с некорректной датой рождения."""
        with self.assertRaises(ValueError):
            add_employee("Антон", "Савчук", "anton@mail.com", "1990-01-01", 50000)

    def test_invalid_salary(self):
        """Тест добавления сотрудника с некорректной зарплатой."""
        with self.assertRaises(ValueError):
            add_employee("Антон", "Савчук", "anton@mail.com", "01.01.1990", -50000)

    def test_empty_database_message(self):
        """Тест сообщения при пустой базе данных."""
        employees = get_all_employees()
        self.assertEqual(len(employees), 0)

    def test_delete_last_employee(self):
        """Тест удаления последнего сотрудника."""
        add_employee("Антон", "Савчук", "anton@mail.com", "01.01.1990", 50000)
        employees = get_all_employees()
        emp_id = employees[0][0]
        delete_employee(emp_id)
        employees = get_all_employees()
        self.assertEqual(len(employees), 0)


if __name__ == "__main__":
    unittest.main()
