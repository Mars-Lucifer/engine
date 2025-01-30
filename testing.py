from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# Сценарий 1
def scen_1():
    try:
        driver = webdriver.Chrome()
        start_time = time.time()  # Запускаем таймер

        # Открываем сайт
        driver.get("http://127.0.0.1:5000/")

        # Разворачиваем окно на весь экран
        driver.maximize_window()
        
        # Даем время на загрузку страницы
        time.sleep(1)
        
        # Находим элемент
        btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/a[2]")
        
        # Кликаем по кнопке
        btn.click()

        time.sleep(1)

        btn2 = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/button")

        btn2.click()
        
        # Ждем несколько секунд, чтобы увидеть результат
        time.sleep(1)

    finally:
        end_time = time.time()  # Завершаем таймер
        execution_time = end_time - start_time
        
        # Закрываем браузер
        driver.quit()
        return execution_time


# Сценарий 2
def scen_2():
    try:
        driver = webdriver.Chrome()
        start_time = time.time()  # Запускаем таймер

        # Открываем сайт
        driver.get("http://127.0.0.1:5000/")

        # Разворачиваем окно на весь экран
        driver.maximize_window()
        
        # Даем время на загрузку страницы
        time.sleep(1)
        
        # Получение текущего URL
        current_url = driver.current_url
        # Формирование нового URL
        new_url = current_url + "/command/1"
        # Переход на новый URL
        driver.get(new_url)
        
        # Ждем несколько секунд, чтобы увидеть результат
        time.sleep(1)

    finally:
        end_time = time.time()  # Завершаем таймер
        execution_time = end_time - start_time
        
        # Закрываем браузер
        driver.quit()
        return execution_time


print(f"Время выполнения сценария 1, вариант 1: {scen_1():.2f} секунд")
print(f"Время выполнения сценария 1, вариант 2: {scen_2():.2f} секунд")