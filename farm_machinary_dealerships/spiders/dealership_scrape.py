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
        stores = response.css('.col-xs-6 a::attr(href)').getall()
        for store in stores:
            store_page = response.urljoin(store)
            yield scrapy.Request(url=store_page, callback=self.parse_data)



    def parse_data(self, response):
        company_name = response.css('h1::text').get()
        products = response.css('.dc-store-wrapper')
        details = response.css('.store-header:contains("Contact") ~ div::text').getall()
        details = [x for x in details if x!='\n'] #remove \n
        detail = ','.join(details) #list to string

        address_list = response.css('.store-header:contains("Address") ~ div::text').getall()
        address_list = [x for x in address_list if x != '\n']  # remove \n
        address = ', '.join(address_list)  # list to string with comma

        yield {
            'dealer_name': company_name,
            'contact': detail,
            'address': address,
        }

        for product in products:
            listing_name = product.css('.listing-name > a::text').get()
            listing_price = product.css('.listing-price::text').get()

            yield {
                'listing_name': listing_name,
                'listing_price': listing_price,
            }

            next_page_url = response.css('#panel li:nth-child(6) a::attr(href)').get()
            if next_page_url:
                next_page_url = response.urljoin(next_page_url)
                yield scrapy.Request(url=next_page_url, callback=self.parse_data)


