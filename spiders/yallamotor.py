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
import datetime
import os
from selenium import webdriver
from datetime import datetime,date
from autodata.items import AutodataItem, MetaItem
from scrapy_splash import SplashRequest

class YallamotorSpider(scrapy.Spider):
    name = 'yallamotor'
    allowed_domains = []
    start_urls = ['https://bahrain.yallamotor.com/used-cars/search']

    def parse(self, response):
        yield Request(response.url,callback=self.parse_page,dont_filter = True)
        path = response.xpath('//div[@class="pagination custom_pagination"]/a[@rel = "next"]')
        for a in path:
            url = ''.join(a.xpath('@href').extract()).strip()
            if url != '':
                yield Request(url, callback = self.parse, dont_filter = True)
        pass

    def parse_page(self, response):
        divs = response.xpath("//div[contains(@class,'col-md-8 col-sm-8 col-xs-12 used-car-list')]/div[contains(@class,'pro-name')]")
        for div in divs:
            new_url = ''.join(div.xpath('./a/@href').extract()).strip()
            url_det = ('https://bahrain.yallamotor.com'+ ''.join(new_url)).strip()
            yield Request(url_det, callback = self.parse_data, dont_filter = True)        
    
    def parse_data(self, response):
        print("DONE")
        item=AutodataItem()
        item2 = MetaItem()

        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "Bahrain"
        item["City"] = ""
        item["Seller_Type"] = "Market Places"
        item["Seller_Name"] = "Yallamotors"
        item["Car_URL"] = response.url
        item["Car_Name"] = ''.join(response.xpath('//*[@id="mainContent"]/section[3]/div/div/div[1]/h1/text()').extract()).replace('Used ','').strip()
        item["Year"] = ""
        item["Make"] = item["Car_Name"].split(' ')[0]
        item["model"] = item["Car_Name"].split(' ')[1]
        item["Spec"] = ""
        item["Doors"] = ""
        item["transmission"] =""
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
        item['Price_Currency'] = 'BHD'
        item['asking_price_inc_VAT'] = ''.join(response.xpath('//span[@class="price-count h3 green bold block"]/text()').extract()).strip()
        item['asking_price_ex_VAT'] = ''.join(response.xpath("div[@class = 'col-md-3 used-car-user-info']/span[@class = 'price-count h3 green bold block']/span[@class ='price-count_small']/text()").extract()).strip()
        item['warranty'] = ''
        item['service_contract'] = ''
        item['vat'] = 'yes'
        item['mileage_unit'] = 'km'
        item['engine_unit'] = ''
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
        sel = response.xpath('//div[@class="pull-left text-left"]')
        
        for s in sel:
            key = ''.join(s.xpath("i//text()").extract()).strip()
            value = ''.join(s.xpath("strong[@class='block']//text()").extract()).strip()
            print("@@@@@@@@",value)
            if key == "Location":
                item['City'] = value
            elif key == "Model Year":
                item['Year'] = value
            elif key == "Car Driven":
                item["mileage"] = value
            elif key == "Transmission:":
                item["transmission"] = value
            elif key == "Fuel Type:":   
                item["fuel_type"] = value
            elif key == "Number of Doors":
                item["Doors"] = value.replace('Door', '').strip()
            elif key == "Number of Cylinders":
                item['cylinders'] = value
            elif key == "Body Style:":
                item['bodystyle'] = value
            elif key == "Exterior Color":
                item['colour_exterior'] = value    

        print('########',item['Car_Name'])

        item2['src'] = "bahrain.yallamotor.com"
        item2['name'] = "yallamotor"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']
        yield item
        pass        
