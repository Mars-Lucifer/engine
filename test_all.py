import unittest
from test_code import TestHomePage
import testing

def run_unittests(report_file):
    # Создаем тестовый набор и запускаем его, вывод направляем в report_file
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHomePage)
    runner = unittest.TextTestRunner(stream=report_file, verbosity=2)
    result = runner.run(suite)
    return result

def run_selenium_tests(report_file):
    # Запускаем Selenium‑сценарии и записываем их вывод в report_file
    report_file.write("\nSelenium Tests Output:\n")
    try:
        t1 = testing.scen_1()
        t2 = testing.scen_2()
        report_file.write(f"Время выполнения сценария 1, вариант 1: {t1:.2f} секунд\n")
        report_file.write(f"Время выполнения сценария 1, вариант 2: {t2:.2f} секунд\n")
    except Exception as e:
        report_file.write(f"Ошибка при выполнении Selenium-тестов: {e}\n")

if __name__ == '__main__':
    with open("test_report.txt", "w", encoding="utf-8") as report_file:
        report_file.write("=== Юнит-тесты ===\n")
        run_unittests(report_file)
        report_file.write("\n=== Selenium-тесты ===\n")
        run_selenium_tests(report_file)