from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
from scrapy.linkextractors import LinkExtractor
import json
import re
import uuid
import hashlib
import logging
import subprocess
import requests
import csv
import io
import scrapy
from datetime import datetime
import os
from autodata.items import AutodataItem, MetaItem

class OmanpeSpider(scrapy.Spider):
    name = "omanpe"
    allowed_domains = []
    urls = []
    start_urls = ["http://oman.pe-mb.com/search-results/?model=&body-style=&amount-range-from=20000&amount-range-to=750000&model-year-range-from=2007&model-year-range-to=2019&year-range-from=2007&year-range-to=2019&packs=&location=&showroomids=884&home-page-search=home-page-search#.XP84DtMzbyJ"]

    def parse(self, response):
        last_page = response.xpath("//ul[contains(@class, 'pagination')]/li/span/a[contains(@class, 'page_a_link')]/text()").extract()[-2]
        last = int(last_page)
        for i in range(1, last+1):
            pages = str.join('',('http://oman.pe-mb.com/search-results/?model=&body-style=&amount-range-from=20000&amount-range-to=750000&model-year-range-from=2007&model-year-range-to=2019&year-range-from=2007&year-range-to=2019&packs=&location=&showroomids=884&home-page-search=home-page-search&pages=',str(i)))
            yield(scrapy.Request(pages, callback=self.parse1))

    def parse1(self, response):
        for href in response.xpath("//a[contains(@class,'readmore')]//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
    
    def parse_dir_contents(self, response):

        item = AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "Oman"
        item["City"] = ""
        item["Seller_Type"] = ""
        item["Seller_Name"] = ""
        item["Car_URL"] = response.url
        item["Car_Name"] = ""
        item["Year"] = ""
        item["Make"] = ""
        item["model"] = ""
        item["Spec"] = ""
        item["Doors"] = ""
        item["transmission"] = ""
        item["trim"] = ""
        item["bodystyle"] = ""
        item["other_specs_gearbox"] = ""
        item["other_specs_seats"] = ""
        item["other_specs_engine_size"] = ""
        item["other_specs_horse_power"] = ""
        item["colour_exterior"] = ""
        item["colour_interior"] = ""
        item["fuel_type"] = ""
        item["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
        item["mileage"] = ""
        item["condition"] = ""
        item["warranty_untill_when"] = ""
        item['service_contract_untill_when'] = ''
        item['Price_Currency'] = ''
        item['asking_price_inc_VAT'] = ''
        item['asking_price_ex_VAT'] = ''
        item['warranty'] = ''
        item['service_contract'] = ''
        item['vat'] = 'yes'
        item['mileage_unit'] = ''
        item['engine_unit'] = ''

        item['Last_Code_Update_Date'] = 'Thursday, June 04, 2019'
        item['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
        item['autodata_Make'] = ''
        item['autodata_Make_id'] = ''
        item['autodata_model'] = ''
        item['autodata_model_id'] = ''
        item['autodata_Spec'] = ''
        item['autodata_Spec_id'] = ''
        item['autodata_transmission'] = ''
        item['autodata_transmission_id'] = ''
        item['autodata_bodystyle'] = ''
        item['autodata_bodystyle_id'] = ''
        item['wheel_size'] = ''
        item['top_speed_kph'] = ''
        item['cylinders'] = ''
        item['acceleration'] = ''
        item['torque_Nm'] = ''

        item2['src'] = "oman.pe-mb.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "omanpe"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Source'] = item2['src']

        item['Year'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[1]).split(':')[-1]).strip()
        item['Make'] = 'Mercedes-Benz'
        mod = (response.xpath("//div[contains(@class, 'col_8 content car-detail')]/h2/text()").extract()[0]).split()
        item['model'] = str.join('',(mod[0],mod[1]))
        item['Car_Name'] = item['Make'] + ' ' + item['model']
        item['transmission'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[5]).split(':')[-1]).strip()
        item['trim'] = ((response.xpath("//ul[contains(@class, 'right')]/li/text()").extract()[2]).split(':')[-1]).strip()
        item['bodystyle'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[4]).split(':')[-1]).strip()
        if '/' in item['bodystyle']:
            item['bodystyle'] = 'Coupe/Cabriolet'
        item['wheel_size'] = ''.join(response.xpath('//div[@class="resp-tabs-container"]/div[2]/ul/li[4]/text()').extract()).strip().split(' ')[-1]
        item['warranty'] = ''.join(response.xpath('//div[@class="resp-tabs-container"]/div[2]/ul/li[1]/text()').extract()).split('Warranty : ')[-1].strip().split(',')[0]
        item['service_contract'] = ''.join(response.xpath('//div[@class="resp-tabs-container"]/div[2]/ul/li[2]/text()').extract()).strip().split(' ')[-1]
        item['colour_exterior'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[3]).split(':')[-1]).strip()
        
        item['mileage'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[2]).split(':')[-1]).strip()
        item['mileage_unit'] = 'km'
        item['asking_price_inc_VAT'] = ((response.xpath("//div[contains(@class,'price')]/h3/text()").extract()[0]).split('OMR')[-1]).strip()
        item['Price_Currency'] = 'OMR'
        item['Country'] = ((response.xpath("//ul[contains(@class, 'right')]/li/text()").extract()[0]).split(':')[-1]).strip()
        item['Seller_Name'] = ((response.xpath("//ul[contains(@class, 'right')]/li/text()").extract()[1]).split(':')[-1]).strip()

        yield item
