from selenium import webdriver
from selenium.webdriver.common.by import By
import time, json

# Чтение конфигурации
with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def scen_1():
    try:
        driver = webdriver.Chrome()
        start_time = time.time()  # Запускаем таймер

        driver.get(data['url'])
        driver.maximize_window()
        time.sleep(1)
        
        btn = driver.find_element(By.XPATH, data['xpath_1'])
        btn.click()
        time.sleep(1)
        
        btn2 = driver.find_element(By.XPATH, data['xpath_2'])
        btn2.click()
        time.sleep(1)
    finally:
        end_time = time.time()  # Завершаем таймер
        execution_time = end_time - start_time
        driver.quit()
        return execution_time

def scen_2():
    try:
        driver = webdriver.Chrome()
        start_time = time.time()  # Запускаем таймер

        driver.get(data['url'])
        driver.maximize_window()
        time.sleep(1)
        
        current_url = driver.current_url
        new_url = current_url + data['link']
        driver.get(new_url)
        time.sleep(1)
    finally:
        end_time = time.time()  # Завершаем таймер
        execution_time = end_time - start_time
        driver.quit()
        return execution_time

if __name__ == '__main__':
    print(f"Время выполнения сценария 1, вариант 1: {scen_1():.2f} секунд")
    print(f"Время выполнения сценария 1, вариант 2: {scen_2():.2f} секунд")