# -*- coding: utf-8 -*-
import scrapy


class CrawlerdSpider(scrapy.Spider):
    name = 'crawlerd'
    allowed_domains = []
    start_urls = []

    file_websites = 'source/websites.txt'

    ignored_extensions = [
        # images
        'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
        'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

        # audio
        'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

        # video
        '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
        'm4a',

        # other
        'css', 'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar',
    ]

    def __init__(self, *args, **kwargs):
        super(CrawlerdSpider, self).__init__(*args, **kwargs)

        if hasattr(self, website):
            urls = self.website.strip().split(';')
        else:
            # parse url list
            self.log('Load website list')
            # load start_urls dari file websites
            with open(self.file_websites, 'r') as f:
                urls = f.read().strip().split('\n')

        for url in urls:
            self.start_urls.append(url)

            if 'http' in url:
                domain = url.split('/')[2].replace('www.', '')
            else:
                domain = url

            self.allowed_domains.append(domain)

    def parse(self, response):
        url = response.url

        # get domain
        domain = url.split('/')[2]#.replace('www.', '')

        try:
            body = response.xpath('normalize-space(//body)').extract_first()
        except:
            return

        for href in response.css('a::attr(href)'):
            url = href.get()

            # cek apakah url atau file
            ext = url.split('.')[-1].lower()
            if ext in self.ignored_extensions:
                continue

            if 'http' not in url:
                yield response.follow(href, self.parse)
                continue

            if len(url.split('/')) >= 3:
                url_domain = url.split('/')[2]
            else:
                self.log(url)
                url_domain = url

            url_domain_nw = url_domain.replace('www.', '')
            if url_domain in self.allowed_domains or url_domain_nw in self.allowed_domains:
                yield response.follow(href, self.parse)
                continue