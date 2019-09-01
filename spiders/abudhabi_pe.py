# -*- coding: utf-8 -*-
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
from dateutil.relativedelta import relativedelta
import os
from autodata.items import AutodataItem, MetaItem

class AbudhabiPeSpider(scrapy.Spider):
    name = "abudhabi_pe"
    allowed_domains = []
    start_urls = ["http://abu-dhabi.pe-mb.com/models/"]

    def parse(self,response):
        models = response.xpath('.//a[@class="view-all"]/@href').extract()
        print(len(models))
        for model in models:
            yield Request(model, callback = self.parse_model, dont_filter = True)
        pass

    def parse_model(self, response):
        yield Request(response.url, callback = self.parse_cars, dont_filter = True)
        pages = ''.join(response.xpath('//div[@class="col_8 content pre-owned"]/div[1]//a[@class="next"]/@href').extract())
        if pages != '':
            yield Request(pages, callback = self.parse_model, dont_filter = True)

    def parse_cars(self, response):
        cars = response.xpath('//a[@class="readmore"]/@href').extract()
        for car in cars:
            yield Request(car, callback = self.parse_data, dont_filter = True)

    def parse_data(self, response):
        item=AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = ""
        item["City"] = ""
        item["Seller_Type"] = ""
        item["Seller_Name"] = ""
        item["Car_URL"] = ""
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
        item['Last_Code_Update_Date'] = 'June 15, 2019'
        item['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')
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

        item2['src'] = "abu-dhabi.pe-mb.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "abudhabi_pe"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']

        item['Year'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[1]).split(':')[-1]).strip()
        item['Make'] = 'Mercedes-Benz'
        mod = (response.xpath("//div[contains(@class, 'col_8 content car-detail')]/h2/text()").extract()[0]).split()
        item['model'] = str.join('',(mod[0],mod[1]))
        item['Car_Name'] = item['Make'] + ' ' + item['model']
        size = len(response.xpath("//ul[contains(@class, 'left')]/li/text()").extract())
        if size>5:
            item['transmission'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[5]).split(':')[-1]).strip()
        item['trim'] = ((response.xpath("//ul[contains(@class, 'right')]/li/text()").extract()[2]).split(':')[-1]).strip()
        item['bodystyle'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[4]).split(':')[-1]).strip()
        item['colour_exterior'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[3]).split(':')[-1]).strip()
        
        item['mileage'] = ((response.xpath("//ul[contains(@class, 'left')]/li/text()").extract()[2]).split(':')[-1]).strip()
        item['mileage_unit'] = 'km'
        item['asking_price_inc_VAT'] = ((response.xpath("//div[contains(@class,'price')]/h3/text()").extract()[0]).split('AED')[-1]).strip()
        item['Price_Currency'] = 'AED'
        item['Country'] = 'UAE'
        item['City'] = ((response.xpath("//ul[contains(@class, 'right')]/li/text()").extract()[0]).split(':')[-1]).strip()
        item['Seller_Name'] = ((response.xpath("//ul[contains(@class, 'right')]/li/text()").extract()[1]).split(':')[-1]).strip()
        arr = response.xpath("//ul/li/text()").extract()
        for i in range(0,len(arr)):
            if "Warranty :" in arr[i]:
                war = ((arr[i]).split('Warranty :')[-1]).strip()
                item['warranty'] = (war.split(',')[0]).strip()
                item['warranty_untill_when'] = (war.split(',')[-1]).strip()
            elif "Wheel Size" in arr[i]:
                item['wheel_size'] = ((arr[i]).split('Wheel Size :')[-1]).strip()
            elif "With a service package" in arr[i]:
                item['service_contract'] = ((arr[i]).split('With a service package :')[-1]).strip()
        
        item['warranty_untill_when'] = (datetime.today() + relativedelta(years=+int(item['warranty_untill_when'].split(' ')[0]))).strftime('%Y-%m-%d')
        yield item

