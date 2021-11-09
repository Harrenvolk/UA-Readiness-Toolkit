from win32com.client import Dispatch
import requests
import wget
import zipfile
import os

def get_chrome_version():
    path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    parser = Dispatch("Scripting.FileSystemObject")     
    version = parser.GetFileVersion(path)     
    return version

def download_chrome_driver():
    # get the chrome driver version number first 3 parts
    chrome_version = get_chrome_version()
    release_version = chrome_version[:chrome_version.rfind(".")]
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + release_version 
    response = requests.get(url)
    version_number = response.text

    # build the donwload url
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"
    print(download_url)
    # download the zip file using the url built above
    latest_driver_zip = wget.download(download_url,'chromedriver.zip')

    # extract the zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall("browser_driver_test") # you can specify the destination folder path here
    # delete the zip file downloaded above
    os.remove(latest_driver_zip)

def get_urls(text):
    urls = []
    words = text.split()
    for word in words:
        if '.' in word:
            urls.append(word)
    return urls

def detect_chrome():
    return os.path.exists("C:\Program Files\Google\Chrome\Application\chrome.exe")

def detect_firefox():
    return os.path.exists("C:\Program Files\Mozilla Firefox")

def detect_edge():
    return os.path.exists("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

def get_browsers():
    browsers = []
    if detect_chrome():
        browsers.append("Chrome")
    if detect_firefox():
        browsers.append("Firefox")
    if detect_edge():
        browsers.append("Edge")
    return browsers
