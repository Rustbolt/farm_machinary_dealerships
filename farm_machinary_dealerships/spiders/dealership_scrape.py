import scrapy


class DealershipScrapeSpider(scrapy.Spider):
    name = 'dealership_scrape'
    allowed_domains = ['machinerypete.com']
    start_urls = ['https://www.machinerypete.com/dealerships/search']

    def parse(self, response):
        states = response.css('.btn.btn-default.btn-xs::attr(href)').getall()
        for state in states:
            state_page = response.urljoin(state)
            yield scrapy.Request(url=state_page, callback=self.parse_stores)



    def parse_stores(self,response):
        stores = response.css('.col-xs-6 > ul > li > a::attr(href)').getall()
        for store in stores:
            store_page = response.urljoin(store)
            yield scrapy.Request(url=store_page, callback=self.parse_data)



    def parse_data(self, response):
        details = response.css('.col-sm-3.col-xs-12')
        for detail in details:
            header = detail.css('.store-header::text').get()
            item = detail.css('.store-item::text').getall()

            yield {
                header: item,
            }
