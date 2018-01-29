# -*- coding: utf-8 -*-
import scrapy


class ListingbotSpider(scrapy.Spider):
    name = 'listingbot'
    allowed_domains = ['ny.mypublicnotices.com']
    start_urls = ['http://ny.mypublicnotices.com/PublicNotice.asp?Page=SEARCHRESULTS']
    url = 'http://ny.mypublicnotices.com/PublicNotice.asp?Page=SEARCHRESULTS'
    page_num = 1
    page_max = 20

    def parseText(self, listing):
        body = listing.extract()
        try:
            address = body.split('known as')[1]
            address = address.split('NY')[0]
            address = address + 'NY'
            
            return {
		'address': address
	    }
        except:
            pass

    def parse(self, response):
        for listing in response.css(".SearchResults1::text"):
            yield self.parseText(listing)

        for listing in response.css(".SearchResults2::text"):
            yield self.parseText(listing)

        self.page_num += 1

        payload = {
            'PageNo': str(self.page_num),
            'DateRange': '',
            'Category': '1',
            'Keyword': '',
            'SearchType': '1',
            'Newspaper': '0',
            'State': 'NY',
            'StartDate': '',
            'EndDate': '',
            'Count': '100',
            'FullTextType': '0',
            'PrintNoticeList': ''
        }

        if self.page_num < self.page_max:
            request = scrapy.FormRequest(
                url=self.url,
                method='POST',
                formdata= payload,
                callback=self.parse)
            request.meta['page_num'] = self.page_num
            request.meta['url'] = self.url
            yield request
