from google_handler.util import Utilities
from selenium.webdriver.common.by import By
import pprint
import logging

class GoogleSearchPageLocators:
    anchor_tags = 'g-card a'


class GoogleJobsPageLocators:
    clear_search_button = 'button.gb_jf'
    search_button = 'button.gb_gf'
    search_input_element = "hs-qsb"
    jobs_cards = 'li'
    result_title = 'div.BjJfJf'
    date_and_time = '//div[@class="oNwCmf"]/div[4]/div[1]/span[2]'
    publisher = '[class*=vNEEBe]'


class Handler(GoogleSearchPageLocators, GoogleJobsPageLocators, Utilities):
    
    def __init__(self, driver):
        self.driver = driver
        self.keyword = ""
        super().__init__(filename='output')
            

    def load_google_jobs_page(self):
        search_page_url = "https://www.google.com/search?q=google+jobs"
        self.driver.get(search_page_url)
        # fish out the "/d+ more jobs" link on the g-card tag
        anchor_tag_elements = self.driver.find_elements(By.CSS_SELECTOR ,self.anchor_tags)
        # first let's assume it's always going to be the last anchor tag
        more_jobs_element = anchor_tag_elements[-1]
        google_jobs_url = more_jobs_element.get_attribute('href')
        self.driver.get(google_jobs_url)

    def fish_out_needed_data(self, card, keyword):
        datetime_of_search = self.now
        result_title = card.find_element(By.CSS_SELECTOR, self.result_title).text
        date_and_time = card.text.split("\n")[-2]
        publisher = card.find_element(By.CSS_SELECTOR, self.publisher).text
        add_via = card.find_elements(By.CSS_SELECTOR, 'div.Qk80Jf')

        data_to_send_to_writer = {
            "Date & time of search": datetime_of_search,
            "Date/Time": date_and_time,
            "Keyword": keyword,
            "Publisher": publisher,
            "Result_Title": result_title,
            "Address": add_via[0].text,
            "Via": add_via[1].text,
        }
        
        pprint.pprint(data_to_send_to_writer)
        self.write_to_sheet(data_to_send_to_writer)

    def scroll_bar_solution(self, job_cards):
        # cap is the highest number of data the bot will fetch
        cnt, o, cap = 1, 10, 500

        while True:

            try:
                card = job_cards[cnt - 1]
                self.scroll_element_into_view(self.driver, card)
            except IndexError as err:
                break

            self.fish_out_needed_data(card, self.keyword)

            if (cnt % o) == 0:  # this will trigger on the 10th item
                self.nap()
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, self.jobs_cards)

                if cnt == len(job_cards):
                    logging.info("\aNew data isn't coming in.")
                    break

            if cnt == cap:
                break

            cnt += 1

    def keyword_jobsearch(self, key):
        self.keyword = key
        
        # input the search word into the input element

        self.clear_search_input_element(self.driver, GoogleJobsPageLocators)
        self.driver.find_element(By.ID, self.search_input_element).send_keys(self.keyword)
        self.click_search_button_element(self.driver, GoogleJobsPageLocators)

        job_cards = self.driver.find_elements(By.TAG_NAME, self.jobs_cards)
        if job_cards:
            self.scroll_bar_solution(job_cards)
            self.close_workbook()
        else:
            print("No jobs match your search at the moment")
