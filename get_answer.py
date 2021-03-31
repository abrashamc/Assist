from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup


class Fetcher:
    def __init__(self, url):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(
            executable_path='drivers/chromedriver',
            chrome_options=self.options)
        self.driver.wait = WebDriverWait(self.driver, 5)
        self.url = url

    def lookup(self):
        """
        Looks for response through google search engine
        """
        self.url = self.url.replace(" ", "%20")
        print("Fetching URL: " + self.url)
        self.driver.get(self.url)
        try:
            self.driver.wait.until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//input[@aria-label=\'Search\' and @class=\'gLFyf gsfi\']")
            ))
        except TimeoutException or NoSuchElementException:
            print("Failed to load page!")

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        try:
            # needs training
            answer = soup.findAll(class_="hgKElc")[0]
        except IndexError as e:
            with open("webpage.html", "w+") as file:
                file.write(str(soup))

        if not answer:
            answer = "I don't know"

        self.driver.quit()
        return answer.get_text()
