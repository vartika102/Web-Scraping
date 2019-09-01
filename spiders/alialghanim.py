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
#from alialghanim.items import AlialghanimItem
from autodata.items import AutodataItem, MetaItem


class AlialghanimSpider(scrapy.Spider):
    name = "alialghanim"
    allowed_domains = []
    urls = []
    start_urls = ["https://alialghanimsons.com.kw/used-cars/"]
    
    
    
    def parse(self,response):
        for href in  response.xpath("//div[contains(@class,'content')]/a[contains(@class,'button white darker')]//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
    
    
    def parse_dir_contents(self,response):
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

        item2['src'] = "alialghanimsons.com.kw"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "alialghanim"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']

        #item2 = MetaItem()
        #       getting make
        item['Car_Name'] =  response.xpath("//div[contains(@class,'details')]/h1/text()").get()
        if "Rolls-Royce" in item['Car_Name']:
            item['Make'] = "Rolls Royce"
            item['model'] = (item['Car_Name'].replace('Rolls-Royce','')).strip()
        elif "McLaren" in item['Car_Name']:
            item['Make'] = "MCLAREN"
            item['model'] = (item['Car_Name'].replace('McLaren','')).strip()
        elif "BMW" in item['Car_Name']:
            item['Make'] = "BMW"
            item['model'] = (item['Car_Name'].replace('BMW','')).strip()
        elif "Range Rover" in item['Car_Name']:
            item['Make'] = "Land Rover"
            item['model'] = item['Car_Name']
        elif "MINI" in item['Car_Name']:
            item['Make'] = "MINI"
            item['model'] = (item['Car_Name'].replace('MINI','')).strip()
        else:
            item['Make'] = "Land Rover"
            item['model'] = item['Car_Name']
                    
        item['Seller_Name'] = 'Ali Alghanim & Sons Automotive'
        item['Seller_Type'] = 'Large Independent Dealers'
        item['Car_URL'] = response.url
        #item['Make'] =
        #item['model'] =
        #item['Spec'] =
        item['asking_price_inc_VAT'] = ((response.xpath("//div[contains(@class,'sales')]/span[contains(@class,'price')]/text()").extract()[0]).split('KD')[0]).strip()
        item['Price_Currency'] = 'KD'
        info = response.xpath("//span[contains(@class,'spec')]/text()").extract()
        col = response.xpath("//span[contains(@class,'spec')]/b/text()").extract()
        for i in range(0,len(col)):
            attr = (col[i].split(':')[0]).strip()
            if attr=="Year":
                item['Year'] = info[i].strip()
            if attr=="Mileage":
                item['mileage'] = (info[i].split('km')[0]).strip()
            if attr=="Capacity":
                item['other_specs_engine_size'] = (info[i].split('cc')[0]).strip()
                item['engine_unit'] = 'cc'
            if attr=="Transmission":
                item['transmission'] = info[i].strip()
            if attr=="Exterior Color":
                item['colour_exterior'] = info[i].strip()
            if attr=="Interior Color":
                item['colour_interior'] = info[i].strip()
            if attr=="Horsepower":
                item['other_specs_horse_power'] = info[i].strip().split(' ')[0]
            if attr=="Cylinders/Valves":
                item['cylinders'] = info[i].split('/')[0].strip()
            if attr=="Torque":
                item['torque_Nm'] = info[i].strip().split(' ')[0]
            if attr=="Top speed":
                item['top_speed_kph'] = info[i].strip().split(' ')[0]
            if attr=="Acceleration 0-100 kph":
                item['acceleration'] = info[i].strip().split(' ')[0]

        item['mileage_unit'] = 'km'
        item['engine_unit'] = 'cc'
        item['Country'] = 'Kuwait'
        
        
        #item2['src'] = "cadillac.mannaiautos.com"
        #item2['ts'] = datetime.datetime.utcnow().isoformat()
        #item2['name'] = "cadillac"
        #item2['url'] = url
        #item2['uid'] = str(uuid.uuid4())
        #item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True)).hexdigest()
        
        #extras=response.xpath("//div[contains(@class, 'extras')]/p/text()").extract()
        #n=len(extras)
        
        #for i in range(0,n):
        #   a=extras[i]
        #   item['ADDITIONAL_INFO'].append(a)
        
        
        yield item



