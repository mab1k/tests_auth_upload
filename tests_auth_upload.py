import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
import time
import os

PATH_CHROME_DRIVER = '/usr/bin/chromedriver'
PROXY = '--proxy-server=http://192.168.4.219:3130'
URL = "http://192.168.4.17/newdesign_old/main/"
FILE_PATH = "/home/user/selenium/test.txt"

@pytest.fixture(scope="module")
def driver():
    service = Service(PATH_CHROME_DRIVER)

    chrome_options = Options()
    chrome_options.add_argument(PROXY) 
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox') 
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    
    yield driver
   
    driver.quit()
    
def login(driver):
    try:
        driver.get(URL)  

        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "siteAuto"))
        )
        button.click()

        login_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "floatingInput"))
        )
        login_input.send_keys("pupa")

        password_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "floatingPassword"))
        )
        password_input.send_keys("123")

        button_auth = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "authBtn"))
        )
        button_auth.click()
    except Exception:
        pytest.fail("Авторизация прошла не успешно")
        
   
def test_registration(driver):
    login(driver)
    
    time.sleep(5)

    
@pytest.mark.dependency(depends=["test_registration"])
def test_upload_file(driver):
    try:
        student_menu_trigger = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'Dropbtn nav-link active') and .//span[text()='Студентам']]"))
        )

        actions = ActionChains(driver)
        actions.move_to_element(student_menu_trigger).perform()
        
        time.sleep(2)  
        
        link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, ".//a[contains(text(), 'Страницы по дисциплинам')]"))
        )
        
        driver.execute_script("arguments[0].click();", link)
        
        button_disc = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.accordion-button.mb-0[data-bs-target='#collapse2044']"))
        )   
        
        driver.execute_script("arguments[0].click();", button_disc)
        
        button_disc2 = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='text-break border-0 w-100 disc_card' and @type='submit']"))
        )
        
        button_disc2.click()
        
        label_element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "cursexchangeshow"))
        )
        
        label_element.click()

        time.sleep(2)

        driver.execute_script("document.getElementById('file1-1589').classList.remove('d-none');")

        upload_element = WebDriverWait(driver, 15).until(
             EC.visibility_of_element_located((By.ID, "file1-1589"))
        )    

        file_path = os.path.abspath(FILE_PATH)
        if not os.path.exists(file_path):
             pytest.fail(f"Файл не найден: {file_path}")

        upload_element.send_keys(file_path)
       
        upload_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.w-100.mt-3.succsesbtn"))
         )

        upload_button.click()
        
        header = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//h3"))
        )
    
        header_text = header.text.strip()

        if header_text != "Подтверждение отправки на проверку":
            print(header_text)
            pytest.fail("Находимся на странице, которая не является послезагрузочной ")

    except Exception:
        pytest.fail("Файл не загружен")