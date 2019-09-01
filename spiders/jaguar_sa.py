
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
#from jaguar.items import JaguarItem
from autodata.items import AutodataItem, MetaItem

class MySpider(Spider):
    name = 'jaguar_sa'
    start_urls = ['http://approved.me.jaguar.com/en_qa/used/saudi-arabia?_ga=2.158721594.1266032569.1556196277-1748026362.1556196277']
    urls= ['http://approved.me.jaguar.com/en_qa/used/saudi-arabia?_ga=2.158721594.1266032569.1556196277-1748026362.1556196277']
##    start_urls = ['http://approved.me.jaguar.com/en_qa/saudi-arabia/used/2018/jaguar/xj/Mohamed_Yousuf_Naghi_Motors_-_Al_Khobar_/_Dammam-110413']
##    urls= ['http://approved.me.jaguar.com/en_qa/saudi-arabia/used/2018/jaguar/xj/Mohamed_Yousuf_Naghi_Motors_-_Al_Khobar_/_Dammam-110413']
  
    
    def start_requests(self):
        for url in self.urls:
            yield SplashRequest(url,callback=self.parse,endpoint='render.html',args={'wait':'5'})

        

    def parse(self, response):
        print("##################")
        body = response.body
        links = response.xpath("//div[contains(@class,'results__vehicle column--nopadding small-12 medium-4 large-3 ')]/a[1]/@href").extract()
        links = list(OrderedDict.fromkeys(links))
        #print(len(links))
        for link in links:
            web= "http://approved.me.jaguar.com"+link
            #yield SplashRequest(web,callback=self.getdata,endpoint='render.html', args={'wait':'15'},headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
            yield Request(web, callback=self.getdata, dont_filter = True)
            #yield SplashRequest(web,callback=self.getdata,endpoint='render.html', args={'wait':'15'}, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'})

    def getdata(self,response):
        print("******************")
        item=AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "KSA"
        item["City"] = ""
        item["Seller_Type"] = "Official Dealers"
        item["Seller_Name"] = "Universal Motor Agencies"
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
        item['warranty'] = 'yes'
        item['service_contract'] = ''
        item['vat'] = 'yes'
        item['mileage_unit'] = ''
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

        item2['src'] = "approved.me.jaguar.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "jaguar_sa"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']
        
        item["Country"] = "Saudi Arabia"
        c=0
        d=0
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "MOHAMED YOUSUF NAGHI MOTORS"
        item["Car_URL"] = response.url

        name = response.xpath("//hgroup/h1[contains(@class,'section-title')]/text()").get().split()[0]
        arr = response.xpath("//tr/td/text()").extract()
        key = response.xpath("//tr/th/text()").extract()
        for k in range(len(key)):
            if 'Model Year' in key[k]:
                item["Year"] = arr[k]
            elif 'Exterior' in key[k]:
                item["colour_exterior"] = arr[k]
            elif 'Interior' in key[k]:
                item["colour_interior"] = arr[k]
            elif 'Kilometers' in key[k]:
                item['mileage'] = arr[k].split(' ')[0]
                item['mileage_unit'] = arr[k].split(' ')[-1]
            elif 'Transmission' in key[k]:
                item["transmission"] = arr[k].split(' ')[-1]
            elif 'Bodystyle' in key[k]:
                item["bodystyle"] = arr[k].split(' ')[-1]
                #item["Doors"] = arr[k].split(' ')[0]
                d = k
            elif 'Engine' in key[k]:
                item["other_specs_engine_size"] = arr[k].split(' ')[0]
                item['cylinders'] = arr[k].split(' ')[1]
                c=k
                item['engine_unit'] = 'l'
            elif 'Fuel Type' in key[k]:
                item["fuel_type"] = arr[k]
            elif 'Location' in key[k]:
                item["City"] = arr[k]
        
        item["Make"] = "Jaguar"
        item["Car_Name"] = item["Make"] + ' ' + ''.join(response.xpath('//hgroup/h1[@class="section-title"]/text()').extract()).replace(arr[c].upper() + ' ','').replace(arr[d].upper(),'').strip()
        item['Price_Currency'] = 'SAR'
        item['asking_price_inc_VAT'] = response.xpath("//strong[contains(@class,'price-box')]/text()").get().split('SAR')[-1].strip()
        yield item   

    

