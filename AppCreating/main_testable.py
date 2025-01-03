import sqlite3
from datetime import datetime
import re
import os
import sys

def get_database_path():
    """Возвращает путь к базе данных в текущей папке."""
    if getattr(sys, 'frozen', False): 
        base_dir = os.path.dirname(sys.executable)
    else: 
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "employees.db")

def initialize_database():
    """Инициализация базы данных."""
    db_path = os.path.join(os.path.dirname(__file__), "employees.db")
    if not os.path.exists(db_path):
        print("База данных не найдена. Создаю новую...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        birth_date TEXT NOT NULL,
                        salary REAL NOT NULL
                      )''')
    conn.commit()
    conn.close()
    print(f"База данных готова. Путь: {db_path}")

def validate_date(date_str):
    """Проверка корректности формата даты."""
    try:
        valid_date = datetime.strptime(date_str, "%d.%m.%Y")
        return valid_date.strftime("%Y-%m-%d") 
    except ValueError:
        return None

def validate_email(email):
    """Проверка корректности email."""
    pattern = r"^[\w.-]+@[\w.-]+\.(ru|com|org|net|gov|edu)$"
    return re.match(pattern, email) is not None

def validate_salary(salary):
    """Проверка корректности зарплаты."""
    try:
        salary = float(salary)
        return salary > 0
    except ValueError:
        return False

def view_employees():
    """Просмотр всех сотрудников с выравниванием столбцов."""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()

    if employees:
        for emp in employees:
            print(f"| {1:<2}| {'ИД':<15}| {emp[0]:<15}")
            print(f"| {2:<2}| {'Имя':<15}| {emp[1]:<15}")
            print(f"| {3:<2}| {'Фамилия':<15}| {emp[2]:<15}")
            print(f"| {4:<2}| {'Email':<15}| {emp[3]:<15}")
            print(f"| {5:<2}| {'Дата рождения':<15}| {emp[4]:<15}")
            print(f"| {5:<2}| {'Зарплата':<15}| {emp[5]:<,.2f}")
            print("-" * 50) 
    else:
        print("Сотрудники не найдены.")

def add_employee(first_name, last_name, email, birth_date, salary):
    """Добавление нового сотрудника."""
    db_path = get_database_path()

    if not first_name or not last_name:
        raise ValueError("Имя и фамилия не могут быть пустыми.")

    if not validate_email(email):
        raise ValueError("Некорректный email.")

    formatted_date = validate_date(birth_date)
    if not formatted_date:
        raise ValueError("Некорректный формат даты. Используйте дд.мм.гггг.")

    if not validate_salary(salary):
        raise ValueError("Зарплата должна быть числом больше 0.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (first_name, last_name, email, birth_date, salary) VALUES (?, ?, ?, ?, ?)",
                   (first_name, last_name, email, formatted_date, salary))
    conn.commit()
    conn.close()
    print("Сотрудник успешно добавлен.")

def delete_employee(emp_id):
    """Удаление сотрудника."""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    if cursor.rowcount == 0:
        print("Сотрудник с таким ID не найден.")
    else:
        print("Сотрудник успешно удален.")
    conn.commit()
    conn.close()

def get_all_employees():
    """Получение всех сотрудников."""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return employees

def update_employee_field(emp_id, field, value):
    """Обновление конкретного поля сотрудника."""
    allowed_fields = ["first_name", "last_name", "email", "birth_date", "salary"]
    if field not in allowed_fields:
        raise ValueError(f"Недопустимое поле для обновления: {field}")

    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE employees SET {field} = ? WHERE id = ?", (value, emp_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Программа готова к тестированию.")
