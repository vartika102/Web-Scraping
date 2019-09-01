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
#from beh.items import BehItem
from autodata.items import AutodataItem, MetaItem

class BehbaniusedSpider(scrapy.Spider):
    name = "behbaniused"
    allowed_domains = []
    urls = []
    start_urls = ["http://behbehaniusedcars.com/vehicles/"]
    

    
    def parse(self, response):
        last_page = ((response.xpath("//div[contains(@class,'wp-pagenavi')]/span[contains(@class,'pages')]/text()").extract()[0]).split('of')[-1]).strip()
        last = int(last_page)
        for i in range(1, last+1):
            pages = str.join('',('http://behbehaniusedcars.com/vehicles/page/',str(i),'/'))
            yield(scrapy.Request(pages, callback=self.parse1))


    def parse1(self, response):
        for href in response.xpath("//div[contains(@class,'listing-detail double')]/a//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
    
    
    def parse_dir_contents(self, response):
        item=AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "Bahrain"
        item["City"] = "Sitra"
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
        item['vat'] = ''
        item['mileage_unit'] = ''
        item['engine_unit'] = 'l'
        item['Last_Code_Update_Date'] = 'Thursday, June 07, 2019'
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

        item2['src'] = "behbehaniusedcars.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "behbaniused"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']

        #       getting make
        #item['Car_Name'] = response.xpath("//div[contains(@class, 'col_8 content car-detail')]/h2/text()").extract()[0].strip()
        item['Car_Name'] = ''.join(response.xpath("//div[contains(@id,'listings')]/h2/text()").extract()).replace('(Approved)','').replace('“','').replace('”','').replace("Approved",'').strip()
        #item['Car_Name'] = re.sub(r'[^a-zA-Z0-9./]', r'', item['Car_Name'])
        item['Year'] = response.xpath("//ul[contains(@class,'specs')]/li/text()").extract()[1].strip()
        
        item['Make'] = ''.join(response.xpath('//p[@class="showroom"]/text()').extract()).split('Showroom')[0].strip()
        if 'used car' in item['Make'].lower() :
                item['Make'] = ''.join(response.xpath("//div[contains(@id,'listings')]/h2/text()").extract()).replace(item['Year'],'').strip().split(' ')[0]
        if 'alfa romeo' in item['Car_Name'].lower():
            item['Make'] = 'Alfa Romeo'
        if 'jetta' in item['Car_Name'].lower():
            item['Make'] = 'Volkswagen'
            item['Car_Name'] = item['Make'] + ' ' + item['Car_Name']
        #item['model'] = ''.join(response.xpath("//div[contains(@id,'listings')]/h2/text()").extract()).strip()
        #item['Spec'] = ''.join(response.xpath("//div[contains(@id,'listings')]/h2/text()").extract()).strip()
        #item['Doors'] =
        item['transmission'] = response.xpath("//ul[contains(@class,'specs')]/li/text()").extract()[3].strip()
        #item['trim'] =
        item['cylinders'] = response.xpath("//ul[contains(@class,'specs')]/li/text()").extract()[6].strip().split(' ')[0]
        item['bodystyle'] = response.xpath("//ul[contains(@class,'specs')]/li/text()").extract()[7].strip()
        #item['other_specs_gearbox'] =
        #item['other_specs_seats'] =
        item['other_specs_engine_size'] = response.xpath("//ul[contains(@class,'specs')]/li/text()").extract()[4].strip().replace('L','').replace('TC','').replace('SC','').replace('T','')
        if len(item['other_specs_engine_size']) > 3:
            item['engine_unit'] = 'cc'
        #item['other_specs_engine_size'] = re.search(r'\d+', item['other_specs_engine_size']).group()
        #item['other_specs_horse_power'] =
        #item['colour_exterior'] =
        #item['fuel_type'] =
        item['mileage'] = response.xpath("//ul[contains(@class,'specs')]/li/text()").extract()[2].strip()
        item['mileage_unit'] = 'km'
        price = response.xpath("//div[contains(@id,'listings')]/h3/text()").extract()[0]
        item['asking_price_inc_VAT'] = ''.join(re.findall(r'\d+',price))
        item['Price_Currency'] = 'BD'
        #item['Country'] =
        #item['City'] =
        item['Seller_Name'] = 'Behbehani Brothers'

        lis = response.xpath('//ul[@id="menu-footer-brands"]/li')
        for li in lis:
            make = ''.join(li.xpath('a/text()').extract()).strip()
            if make in item['Car_Name']:
                item['Make'] = make
        print("############",len(lis))
##        if 'volkswagen' in ''.join(response.xpath('//p[@class="showroom"]/text()').extract()).lower():
##            item['Make'] = 'Volkswagen'
##            item['Car_Name'] = item['Make'] + ' ' + item['Car_Name']
        yield item

