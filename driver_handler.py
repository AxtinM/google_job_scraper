import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def create_driver_handler():
    '''
    creates a browser instance for selenium,
    it adds some functionalities into the browser instance
    '''
    chrome_options = Options()
    chrome_options.add_argument("--lang=en")
    prefs = {'intl.accept_languages': 'en-gb'}
    chrome_options.add_experimental_option("prefs", prefs)

    # the following two options are used to take out the chrome browser infobar
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver_instance = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver_instance.implicitly_wait(10)
    
    return driver_instance

def set_windows_title():
    '''customizes the window title'''
    os.system('title Google Jobs Tool')
    