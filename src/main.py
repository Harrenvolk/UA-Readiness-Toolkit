from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from mss import mss

DELAY = 3
with mss() as sct:

    driver = webdriver.Chrome(executable_path='./chromedriver.exe')

    driver.maximize_window()
    try:
        driver.get('https://համընդհանուր-ընկալում-թեստ.հայ')
    except WebDriverException:
        print("Can't load it!")

    try:
        myElem = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
    except TimeoutException:
        print("Timeout!")

    print("\n\n\n\n ++++++++++++++++++++++++++ \n\n\n\n")
    print(driver.current_url)
    print("\n\n\n\n ++++++++++++++++++++++++++ \n\n\n\n")
    
    sct.shot()
    # Do OCR from this if we have to use image

driver.quit() 