# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
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
from collections import OrderedDict
import os
from autodata.items import AutodataItem, MetaItem

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

class FridaymarketSpider(scrapy.Spider):
    name = 'fridaymarket'
    allowed_domains = []
    start_urls = ['https://qa.fridaymarket.com/cars-vehicles-in-qatar-200']
    
    def parse(self, response):
        yield Request(response.url,callback=self.parse_page,dont_filter = True)
        path = response.xpath('//div[@class="pager"]//div[@class="pagination"]/a[@rel = "next"]')
        url = ''
        for a in path:
            url = ''.join(a.xpath('@href').extract()).strip()
            #print(url)
            urll = ('https://qa.fridaymarket.com'+ ''.join(url)).strip()
            #print(urll)
        if url != '':
            yield Request(urll, callback = self.parse, dont_filter = True)
        pass
        

    def parse_page(self, response):
        divs = response.xpath('//div[@class="panel-body rows ats-block"]/ul/li')
        print(response.url)
        l = 10
        if len(divs) != 11:
            l = len(divs)
        for div in range(l):
            new_url = ''.join(divs[div].xpath('.//div[@class="ad-image"]/a/@href').extract()).strip()
            #print(new_url)
            url_det = ('https://qa.fridaymarket.com'+ ''.join(new_url)).strip()
            yield Request(url_det, callback = self.parse_data, dont_filter = True)
        

        

    def parse_data(self, response):
        item=AutodataItem()
        item2 = MetaItem()
            
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "Qatar"
        item["City"] = ""
        item["Seller_Type"] = "Market Places"
        item["Seller_Name"] = "Friday cars"
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
        item['Price_Currency'] = 'QAR'
        item['asking_price_inc_VAT'] = ''
        item['asking_price_ex_VAT'] = ''
        item['warranty'] = ''
        item['service_contract'] = ''
        item['vat'] = 'yes'
        item['mileage_unit'] = ''
        item['engine_unit'] = ''
        item['Last_Code_Update_Date'] = 'June 22, 2019'
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
            
        
        labels = response.xpath('//td[@class="viewad-label"]')
        values = response.xpath('//span[@class="viewad-data"]')
            
        for lab in range(len(labels)):
            label = ''.join(labels[lab].xpath('text()').extract()).strip()
            value = ''.join(values[lab].xpath('text()').extract()).strip()
            if 'Brand' in label:
                item['Make'] = value
            elif 'Model' in label:
                item['model'] = value
                
            elif 'Year' in label:
                item['Year'] = value
                
            elif 'Location' in label:
                item['City'] = value
                
            elif "Price" in label:
                    
                item["asking_price_inc_VAT"] = value.split(' ')[0]

            
               
            
                
        print(item['Car_Name'])
        item["Car_Name"] = remove_non_ascii(''.join(response.xpath('//div[@class = "panel-body alone pad0 viewad-topinfo"]/h1/text()').extract()).strip())
        print(item['Car_Name'])
        item2['src'] = "http://qa.fridaymarket.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "fridaymarket"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']

        if item['Car_Name'] != '':
            yield item

        pass

        
    


    

    
