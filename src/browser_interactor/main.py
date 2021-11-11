import os
import sys
import pytesseract
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
from mss import mss
from PIL import Image
import argparse

from .utils import get_urls, get_browsers

def generate_screenshot(list_of_domains, list_of_language_codes, browser):
    DELAY = 3
    list_of_image_files = []
    browser_driver_path = r"{}".format(os.environ.get("BROWSER_DRIVER_PATH"))
    driver = None

    if browser == "Chrome":
        browser_driver_path += "chromedriver.exe"
        driver = webdriver.Chrome(executable_path=browser_driver_path)
        driver.get('chrome://settings/clearBrowserData')
        driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
    elif browser == "Firefox":
        browser_driver_path += "geckodriver.exe"
        driver = webdriver.Firefox(executable_path=browser_driver_path)
    elif browser == "Edge":
        browser_driver_path += "msedgedriver.exe"
        driver = webdriver.Edge(executable_path=browser_driver_path)
    
    driver.maximize_window()

    for (domain, language_code) in zip(list_of_domains, list_of_language_codes):    
        with mss() as sct:
            try:
                driver.get("https://"+domain)
                default_html_element = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
            except TimeoutException:
                print("Timeout!")
            except WebDriverException:
                print("Failed to load website., {}".format(domain))
            finally:
                print("\n\n\n\n ++++++++++++++++++++++++++ \n\n\n\n")
                print(driver.current_url)
                print("\n\n\n\n ++++++++++++++++++++++++++ \n\n\n\n")
                screenshot_filename = language_code + ".png"
                screenshot_filename = f"./src/browser_interactor/screenshots/{browser}_{screenshot_filename}"
                sct.shot(output = screenshot_filename)
                list_of_image_files.append(screenshot_filename)
    driver.quit()
    return list_of_image_files

def resize_image(im):
    w,_=im.size
    return im.crop((0, 50, w/2, 120))

def test_ua_readiness(list_of_image_files, list_of_language_codes):
    tesseract_path = r"{}".format(os.environ.get("TESSERACT_PATH"))
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    for (image, language_code) in zip(list_of_image_files, list_of_language_codes):
        text=pytesseract.image_to_string(resize_image(Image.open(image)), lang=language_code)
        textEng=pytesseract.image_to_string(resize_image(Image.open(image)), lang="eng")

        punycodeCount=textEng.count("xn--")
        if punycodeCount>0:
            pass
            # showing in punycode
        else:
            pass
            # normal form
        print("Possible URLS : ", get_urls(text), "\n\n")
        print("Text: \n", text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser', type=str, default="Chrome")
    parser.add_argument('-detect_browsers', action='store_true')
    args = parser.parse_args()

    if args.detect_browsers:
        print("Detected browsers : ")
        for browser in get_browsers():
            print("* ", browser)
        sys.exit(0)

    load_dotenv()
    list_of_domains = ["համընդհանուր-ընկալում-թեստ.հայ","универсальное-принятие-тест.москва","सार्वभौमिक-स्वीकृति-परीक्षण.संगठन"]
    list_of_language_codes = ["hye","rus","hin"]
    print(list_of_domains)

    list_of_image_files = generate_screenshot(list_of_domains, list_of_language_codes, args.browser)
    test_ua_readiness(list_of_image_files, list_of_language_codes)
