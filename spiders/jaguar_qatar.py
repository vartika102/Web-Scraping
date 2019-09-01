import scrapy
from scrapy_splash import SplashRequest
from scrapy.http import Request,FormRequest
import re
import uuid
import hashlib
import logging
import subprocess
import requests
import csv
import io
from scrapy.spiders import Spider
from datetime import datetime
from scrapy.http import Request,FormRequest
import json
from scrapy.http.headers import Headers
import urllib
from collections import OrderedDict
from autodata.items import AutodataItem, MetaItem

class MySpider(Spider):
    name = 'jaguar_qatar'
    start_urls = ["http://approved.me.jaguar.com/en_qa/used/qatar"]
    urls= ['http://approved.me.jaguar.com/en_qa/used/qatar']
    
    def start_requests(self):
        for url in self.urls:
            yield SplashRequest(url,callback=self.parse,args={'wait':'5'},endpoint='render.html')

    def parse(self, response):
        links = response.xpath("//div[contains(@class,'results__vehicle column--nopadding small-12 medium-4 large-3 ')]/a//@href").extract()
        links = list(OrderedDict.fromkeys(links))
        print(links)
        for link in links:
            web= "http://approved.me.jaguar.com"+link
            yield Request(web,callback=self.getdata, dont_filter = True)

    def getdata(self,response):
        item=AutodataItem()
        item2=MetaItem()
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
        item["Last_Code_Update_Date"] = "Wednesday,June 19,2019"
        item["Scrapping_Date"] = datetime.today().strftime('%A, %B %d, %Y')
        item["Car_URL"] = response.url
        item2['src'] = "approved.me.jaguar.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "jaguar_qatar"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Source'] = item2['src']
        
        item['autodata_Make_id'] = ''
        item['autodata_model'] = ''
        item['autodata_model_id'] = ''
        item['autodata_Spec'] = ''
        item['autodata_Spec_id'] = ''
        item['autodata_transmission'] = ''
        item['autodata_transmission_id'] = ''
        item['autodata_bodystyle'] = ''
        item['autodata_bodystyle_id'] = ''
        item["Last_Code_Update_Date"] = "Tuesday,June 25,2019"
        item["Scrapping_Date"] = datetime.today().strftime('%A, %B %d, %Y')
        item["Country"] = "Qatar"
        
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "Alfardan Premier Motors"
        item["Car_URL"] = response.url
        name = response.xpath("//hgroup/h1[contains(@class,'section-title')]/text()").get().split()[0]
        arr = response.xpath("//tr/td/text()").extract()
        item["City"] = arr[8]
        item["Car_Name"] = "Jaguar"+ ' ' + name
        item["Year"] = arr[0]
        item["Make"] = "Jaguar"
        item["model"] = name
        item["transmission"] = arr[4]
        item["bodystyle"] = arr[5]
        item["colour_exterior"] = arr[1]
        item["colour_interior"] = arr[2]
        item["fuel_type"] = arr[7]
        item["mileage"] = arr[3].split('Km')[0]
        item['Price_Currency'] = 'QAR'
        item['asking_price_inc_VAT'] = response.xpath("//strong[contains(@class,'price-box')]/text()").get().split('QAR')[-1].strip()
        yield item

