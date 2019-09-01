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

class DubilSpider(scrapy.Spider):
    name = 'dubil'
    allowed_domains = []
    start_urls = ['https://www.dubicars.com/search?view=&o=&fs=0&fss=0&ma=&mo=0&eo=not-for-export&pf=&pt=&semi=100&emi=&fb=&dp=0&lp=36&l=3&yf=&yt=&kf=&kt=&c=used&st=&b=&f=&g=&cy=&co=&gi=&s=']
    
    def parse(self, response):
        yield Request(response.url,callback=self.parse_page,dont_filter = True)
        nextt = response.xpath("//a[contains(@class,'next')]//@href").get()
        if(nextt is not None):
            yield Request(nextt,callback=self.parse,dont_filter = True)
        pass
    
    def parse_page(self, response):
        pag = response.xpath("//h3/a//@href").extract()
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
        item["Seller_Type"] = "MarketPlace"
        item["Seller_Name"] = "111 Used Cars"
        item["Car_URL"] = response.url
        
        item2['src'] = "dubicars.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "dubi_spider"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Source'] = item2['src']
        
        item['asking_price_inc_VAT'] = response.xpath("//strong[contains(@class,'money')]/text()").extract()[1].split('AED')[-1].strip()
        item['Price_Currency'] = 'AED'
        arr = response.xpath("//tr/td/text()").extract()
        item['Year'] = str(arr[2])
        item['Make'] = str(arr[0])
        item['model'] = arr[1]
        item["Car_Name"] =item['Make']+' '+item['model']
        if item['Car_Name'] != '':
            item['Spec'] = arr[8].strip()
            item['transmission'] = arr[9]
            item['bodystyle'] = arr[5]
            #item['other_specs_horse_power'] =
            item['colour_exterior'] = arr[4]
            item['fuel_type'] = arr[10]
            item['mileage'] = arr[6]
            item['mileage_unit'] = 'km'
            item['colour_interior'] = arr[13]
            item['other_specs_seats'] = arr[11]
            yield item
                
        #item['other_specs_engine_size'] =
        
        














