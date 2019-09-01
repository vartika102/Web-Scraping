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

class EliteSpider(scrapy.Spider):
    name = 'elite'
    allowed_domains = []
    start_urls = ['https://theelitecars.com/pre-owned-used-approved-cars-dubai/']

    def parse(self, response):
        yield Request(response.url,callback=self.parse_page,dont_filter = True)
        nextt = response.xpath("//li/a[contains(@class,'next page-numbers')]//@href").get()
        if(nextt is not None):
            yield Request(nextt,callback=self.parse,dont_filter = True)
        pass

    def parse_page(self, response):
        pag = response.xpath("//div[contains(@class,'inv_title text-left text-uppercase')]/a//@href").extract()
        
        for div in pag:
            url = div
            yield Request(url, callback=self.parse_data, dont_filter = True)

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

        item["Last_Code_Update_Date"] = "Wednesday,June 19,2019"
        item["Scrapping_Date"] = datetime.today().strftime('%A, %B %d, %Y')
        item["Country"] = "UAE"
        item["City"] = "Dubai"
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "The Elite Cars LLC"
        item["Car_URL"] = response.url
        item['asking_price_inc_VAT'] = response.xpath("//div[contains(@class,'car-price')]/h3/text()").extract()[0].split('AED')[-1].strip()
        item['Price_Currency'] = 'AED'
        item["Car_Name"] = response.xpath("//div[contains(@class,'col-lg-6 p-0 car-spec')]/h1/text()").extract()[0].strip()
        if "BMW" in item["Car_Name"]:
            item["Make"] = "BMW"
            item["model"] = item["Car_Name"].split()[1]
        if "AUDI" in item["Car_Name"]:
            item["Make"] = "AUDI"
            item["model"] = item["Car_Name"].split()[1]            
        if "RANGE ROVER" in item["Car_Name"]:
            item["Make"] = "LAND ROVER"
        if "DODGE" in item["Car_Name"]:
            item["Make"] = "DODGE"
            item["model"] = item["Car_Name"].replace('DODGE','').strip()
        if "LAND ROVER" in item["Car_Name"]:
            item["Make"] = "LAND ROVER"
            item["model"] = item["Car_Name"].replace('LAND ROVER','').strip()
        if "MASERATI" in item["Car_Name"]:
            item["Make"] = "MASERATI"
            item["model"] = item["Car_Name"].split()[1]
            item["Spec"] = " ".join(re.findall("[a-zA-Z]+",item["Car_Name"].split()[2]))        
        if "PORSCHE" in item["Car_Name"]:
            item["Make"] = "PORSCHE"
            item["model"] = item["Car_Name"].split()[1]
            sp = item["Car_Name"].replace('PORSCHE','')
            item["Spec"] = sp.replace(item["model"],'').strip()
        if "CADILLAC" in item["Car_Name"]:
            item["Make"] = "CADILLAC"
            item["model"] = item["Car_Name"].replace('CADILLAC','')
        if "CHEVROLET" in item["Car_Name"]:
            item["Make"] = "CHEVROLET"
            item["model"] = item["Car_Name"].split()[1]
            item["Spec"] = item["Car_Name"].split()[2]
        if "JAGUAR" in item["Car_Name"]:
            item["Make"] = "JAGUAR"
            item["model"] = item["Car_Name"].replace('JAGUAR','').strip()
        if "FERRARI" in item["Car_Name"]:
            item["Make"] = "FERRARI"
            item["model"] = item["Car_Name"].replace('FERRARI','').strip()
        if "FORD" in item["Car_Name"]:
            item["Make"] = "FORD"
            item["model"] = item["Car_Name"].split()[1]
            sp = item["Car_Name"].replace('FORD','')
            item["Spec"] = sp.replace(item["model"],'').strip()
        if "JEEP" in item["Car_Name"]:
            item["Make"] = "JEEP"
            item["model"] = item["Car_Name"].replace('JEEP','')
        if "MERCEDES" in item["Car_Name"]:
            item["Make"] = "MERCEDES"
            item["model"] = item["Car_Name"].replace('MERCEDES','').strip()
        if "NISSAN" in item["Car_Name"]:
            item["Make"] = "NISSAN"
            item["model"] = item["Car_Name"].replace('NISSAN','').strip()
            
        arr = response.xpath("//tr/td/text()").extract()        
        arrs = list(OrderedDict.fromkeys(arr))
        for i in range(0,len(arrs)):
            if arrs[i]=='Year':
                item["Year"] = arr[i+1]
            if arr[i]=='Kilometers':
                item["mileage"] = arr[i+1]
                item['mileage_unit'] = 'KM'
            if arr[i]=='Engine':
                item["other_specs_engine_size"] = arr[i+1].split('l')[0]
                item['engine_unit'] ='L'
            if arr[i]=='Horsepower':
                item["other_specs_horse_power"] =arr[i+1]
            if arrs[i]=='Exterior Color':
                item["colour_exterior"] = arrs[i+1]
            if arrs[i]=='Fuel Type':
                item["fuel_type"] = arrs[i+1]
            if arrs[i]=='Warranty':
                item['warranty'] = arrs[i+1]
            if arrs[i]=='Body Type':
                item['bodystyle'] = arrs[i+1]
                    
        item2['src'] = "theelitecars.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "elite"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Source'] = item2['src']
        yield item        
