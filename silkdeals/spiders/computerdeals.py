import scrapy
from scrapy_selenium import SeleniumRequest

class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'
    # allowed_domains = ['slickdeals.net']
    # start_urls = ['http://slickdeals.net/']

    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://slickdeals.net/computer-deals/',
            wait_time = 3,
            callback=self.parse
        )

    def parse(self, response):
        products = response.xpath("//ul[@class='dealTiles categoryGridDeals blueprint']/li")

        for product in products:
            name = product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/text()").get()
            company = product.xpath('.//*[@data-no-linkable="data-no-linkable"]/text()').get()
            price = product.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get()
            link = product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/@href").get()

            yield{
                "product_name": name,
                "product_company": company,
                "product_price": price, 
                "product_link": f"https://slickdeals.net{link}"             
            }

        next_page = response.xpath("//a[@data-role='next-page']/@href").get()

        if next_page:
            absolute_url= f"https://slickdeals.net{next_page}"

            yield SeleniumRequest(
                url=absolute_url,
                wait_time= 3,
                callback=self.parse
            )
