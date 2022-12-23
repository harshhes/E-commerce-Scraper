import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ExampleSpider(scrapy.Spider):
    name = 'example'
   
    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        # img = response.meta['screenshot']

        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)

        driver = response.meta['driver']
        search_input = driver.find_element(By.XPATH,"//input[@id='search_form_input_homepage']")
        search_input.send_keys("Hello World")

        search_input.send_keys(Keys.ENTER)
        # driver.save_screenshot("ss3.png")
        html = driver.page_source
        response_obj = Selector(text=html)

        for link in response_obj.xpath("//h2[contains(@class,'LnpumSThxEWMIsDdAT17')]/a"):
            yield {
                "link": link.xpath(".//@href").get()
            }