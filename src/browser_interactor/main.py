import os
import pytesseract

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from mss import mss
from PIL import Image

def generate_screenshot(list_of_domains, list_of_language_codes):
    DELAY = 3
    list_of_image_files = []
    browser_driver_path = r"{}".format(os.environ.get("BROWSER_DRIVER_PATH"))
    driver = webdriver.Chrome(executable_path=browser_driver_path)
    driver.maximize_window()
    for (domain, language_code) in zip(list_of_domains, list_of_language_codes):    
        with mss() as sct:
            try:
                driver.get("https://"+domain)
                default_html_element = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
                print("\n\n\n\n ++++++++++++++++++++++++++ \n\n\n\n")
                print(driver.current_url)
                print("\n\n\n\n ++++++++++++++++++++++++++ \n\n\n\n")
                screenshot_filename = language_code + ".png"
                sct.shot(output = screenshot_filename)
                screenshot_filename = "./" + screenshot_filename
                list_of_image_files.append(screenshot_filename)
            except TimeoutException:
                print("Timeout!")
            except WebDriverException:
                print("Failed to load website., {}".format(domain))
    driver.quit()
    return list_of_image_files

def test_ua_readiness(list_of_image_files, list_of_language_codes):
    tesseract_path = r"{}".format(os.environ.get("TESSERACT_PATH"))
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    for (image, language_code) in zip(list_of_image_files, list_of_language_codes):
       text=pytesseract.image_to_string(Image.open(image), lang=language_code)
       print(text)



if __name__ == "__main__":
    load_dotenv()
    list_of_domains = ["համընդհանուր-ընկալում-թեստ.հայ","универсальное-принятие-тест.москва","सार्वभौमिक-स्वीकृति-परीक्षण.संगठन"]
    list_of_language_codes = ["hye","rus","hin"]
    print(list_of_domains)
    list_of_image_files = generate_screenshot(list_of_domains, list_of_language_codes)
    test_ua_readiness(list_of_image_files, list_of_language_codes)