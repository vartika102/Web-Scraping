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

class FerrariSpider(scrapy.Spider):
    name = "ferrari"
    allowed_domains = []
    urls = []
    start_urls = ["https://safat.ferraridealers.com/en_gb/used-ferrari"]
    
    def parse(self,response):
        for href in response.xpath("//div[contains(@class, 'vehicle-card__container vehicle-card__container--buttons')]/a[contains(@class,'vehicle-card__button vehicle-card__button--secondary')]//@href"):
            url="https://safat.ferraridealers.com"+href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self,response):
        item=AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "Kuwait"
        item["City"] = ""
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "Ferrari Dealers"
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
        item['vat'] = ''
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

        item2['src'] = "safat.ferraridealers.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "ferrari"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']
        
        item['asking_price_inc_VAT'] = ((response.xpath("//div[contains(@class, 'vehicle-details__item')]/strong[contains(@class, 'vehicle-details__price')]/text()").get()).split('KWD')[-1]).strip()
        item['Price_Currency'] = 'KWD'
        item['Year'] = ((response.xpath("//div[contains(@class, 'vehicle-details__item')]/h1[contains(@class, 'vehicle-details__title')]/text()").extract()[0]).split('Ferrari')[0]).strip()
        mod = ((response.xpath("//div[contains(@class, 'vehicle-details__item')]/h1[contains(@class, 'vehicle-details__title')]/text()").extract()[0]).split('Ferrari')[1]).strip()
        item['Car_Name'] = 'Ferrari' + ' ' + mod
        item['Make'] = 'Ferrari'       
        item['model'] = ((response.xpath("//div[contains(@class, 'vehicle-details__item')]/h1[contains(@class, 'vehicle-details__title')]/text()").extract()[0]).split('Ferrari')[1]).strip()
        item['trim'] = response.xpath("//tr[contains(@class, 'vehicle-spec__row')]/td/text()").extract()[1].strip()
        item['fuel_type'] = response.xpath("//tr[contains(@class, 'vehicle-spec__row')]/td/text()").extract()[6].strip()
        item['transmission'] = response.xpath("//tr[contains(@class, 'vehicle-spec__row')]/td/text()").extract()[2].strip()
        item['mileage'] = ((response.xpath("//tr[contains(@class, 'vehicle-spec__row')]/td/text()").extract()[5]).split('km')[0]).strip()
        item['mileage_unit'] = 'km'
        arr = response.xpath("//li[contains(@class,'accordion__list-item')]/text()").extract()
        for i in range(0,len(arr)):
            if " cc" in arr[i]:
                item['other_specs_engine_size'] = ((arr[i]).split('cc')[0]).strip()
        item['engine_unit'] = 'cc'
        item['colour_exterior'] = response.xpath("//tr[contains(@class, 'vehicle-spec__row')]/td/text()").extract()[0].strip()

        def hasNumbers(inputString):
            return any(char.isdigit() for char in inputString)
        hp = response.xpath("//p[contains(@class, 'vehicle-performance__text')]/text()").extract()[2]
        if hasNumbers(hp)==True:
            d = hp.split('kW')
            item['other_specs_horse_power'] = round(int(d[0][-4:].strip())*1.34102)
        
        item['bodystyle'] = response.xpath("//tr[contains(@class, 'vehicle-spec__row')]/td/text()").extract()[3].replace('2-Door','').strip()

        yield item
