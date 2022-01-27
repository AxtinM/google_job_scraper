from selenium.webdriver.common.by import By
import random
import logging
import time
from xlsxhandler import XlsxWriter
import datetime

class TimeKeeper:
    @property
    def now(self):
        '''
        return the current correct date and time using the format specified
        '''
        return f'{datetime.datetime.now():%d-%b-%Y T%I:%M}'

class Utilities(XlsxWriter, TimeKeeper):

    
    def click_helper(self, driver, selector):
        '''
        this is an helper function that collects a locator and
        clicks that element with that locator
        '''
        element = driver.find_element(By.CSS_SELECTOR, selector)
        element.click()


    def clear_search_input_element(self, driver, locator_class):
        '''
        clears the search input element
        '''
        self.click_helper(driver, locator_class.clear_search_button)


    def click_search_button_element(self, driver, locator_class):
        '''
        clicks the search button
        '''
        self.click_helper(driver, locator_class.search_button)


    def nap(self, secs=random.randrange(1, 10)):
        '''
        sleeps the bot for a random number of seconds
        '''
        logging.info(f"Napping for {secs} seconds")
        time.sleep(secs)


    def scroll_element_into_view(self, driver, element):
        driver.execute_script("arguments[0].scrollIntoView();", element)

   
    

    
