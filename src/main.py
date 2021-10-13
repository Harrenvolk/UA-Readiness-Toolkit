from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from mss import mss
from PIL import Image
import pytesseract


DELAY = 3
with mss() as sct:

    driver = webdriver.Chrome(executable_path=r'C:\Users\srira\Documents\MP\chromedriver.exe')

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
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    text=pytesseract.image_to_string(Image.open('./monitor-1.png'), lang='eng')
    print(text)

driver.quit() 