# -*- coding: utf-8 -*-
import scrapy


class GamelabSpider(scrapy.Spider):
    name = 'gamelab'
    allowed_domains = ['gamelab.id']
    start_urls = ['http://gamelab.id/']

    def parse(self, response):
        url = response.url

        # get domain
        domain = url.split('/')[2]#.replace('www.', '')

        body = response.xpath('normalize-space(//body)').extract_first()

        for href in response.css('a::attr(href)'):
            href = href.get()
            href_domain = href.split('/')[2]
            href_domain_nw = href_domain.replace('www.', '')

            if 'http' not in href or href_domain in self.allowed_domains or href_domain_nw in self.allowed_domains:
                yield response.follow(href, self.parse)