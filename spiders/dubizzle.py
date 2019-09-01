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
from datetime import datetime,date
from collections import OrderedDict
import os
from autodata.items import AutodataItem, MetaItem

class DubizzleSpider(scrapy.Spider):
    name = 'dubizzle'
    allowed_domains = []
    start_urls = ['https://uae.dubizzle.com/motors/used-cars/']

    def parse(self, response):
        made = response.xpath('//div[@class="browse_in_list"]//ul[@class="browse_in_widget_col"]/li/a/@href').extract()
        print("########",len(made), response.url)
        for m in made:
            url = "https://uae.dubizzle.com/motors/used-cars/" + m
            yield Request(url, callback = self.parse_made, dont_filter = True)

    def parse_made(self, response):
        model = response.xpath('//div[@class="browse_in_list "]//ul[@class="browse_in_widget_col"]/li/a/@href').extract()
        for m in model:
            url = response.url + m
            yield Request(url, callback = self.parse_model, dont_filter = True)

    def parse_model(self, response):
        yield Request(response.url,callback=self.parse_page,dont_filter = True)
        nextt = ''.join(response.xpath("//a[contains(@id,'next_page')]//@href").extract())
        if(nextt != ''):
            url = "https://uae.dubizzle.com"+nextt
            yield Request(url,callback=self.parse_model,dont_filter = True)
        pass

    def parse_page(self, response):
        pag = response.xpath("//h3[contains(@id,'title')]//span[contains(@style,'direction: ltr')]/a//@href").extract()
        new = ''.join(response.xpath('//h3[@class="featured-ad-title"]//@href').extract())
        if new != '':
            pag.append(new)
        for div in pag:
            url = div
            yield Request(url, callback=self.parse_data, dont_filter = True)
        pass

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
        item['wheel_size'] = ''
        item['top_speed_kph'] = ''
        item['cylinders'] = ''
        item['acceleration'] = ''
        item['torque_Nm'] = ''
        item["Last_Code_Update_Date"] = "Wednesday,June 19,2019"
        item["Scrapping_Date"] = datetime.today().strftime('%A, %B %d, %Y')
        item["Country"] = "UAE"
        item["City"] = "Dubai"
        item["Seller_Type"] = "MarketPlace"
        item["Seller_Name"] = "111 Used Cars"
        item["Car_URL"] = response.url

        item2['src'] = "dubizzle.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "dubizzle_spider"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Source'] = item2['src']
        
        item["Last_Code_Update_Date"] = "Friday,June 21,2019"
        item["Scrapping_Date"] = datetime.today().strftime('%A, %B %d, %Y')
        item["Country"] = "UAE"
        item["City"] = ""
        item["Seller_Type"] = "Marketplaces"
        item["Seller_Name"] = "Dubizzle"
        item["Car_URL"] = response.url
        url = item["Car_URL"]
        m = url.split('used-cars/')[-1]
        item["Make"] = m.split('/')[0]
        item["model"] = m.split('/')[1]
        item['asking_price_inc_VAT'] = response.xpath("//span[contains(@id,'actualprice')]/text()").get()
        item['Price_Currency'] = 'AED'
        
        item["Car_Name"] = item["Make"]+' ' +item["model"]
        
        arr = response.xpath('//div[@id="listing-details-list"]//li/strong/text()').extract()
        label = response.xpath('//div[@id="listing-details-list"]//li/span/text()').extract()
        for lab in range(len(label)):
            label[lab] = label[lab].strip()
        label = list(filter(None, label))
        
        for i in range(len(arr)):
            if 'Year' in label[i]:
                item["Year"] = arr[i].strip()
            elif 'Kilometers' in label[i]:
                item["mileage"] = arr[i].strip()
                item['mileage_unit'] = 'KM'
            elif 'Color' in label[i]:
                item['colour_exterior'] = arr[i].strip()
            elif 'Doors' in label[i]:
                item['Doors'] = arr[i].split()[0].replace('+','').strip()
            elif 'Warranty' in label[i]:
                item['warranty'] = arr[i].strip()
            elif 'Specs' in label[i]:
                item["Spec"] = arr[i].strip()
            elif 'Transmission' in label[i]:
                item['transmission'] = arr[i].replace('Transmission','').strip()
            elif 'Body Type' in label[i]:
                item['bodystyle'] = arr[i].strip()
            elif 'Fuel Type' in label[i]:
                item["fuel_type"] = arr[i].strip()
            elif 'Trim' in label[i]:
                item['trim'] = arr[11].strip()
            elif 'Cylinders' in label[i]:
                item['cylinders'] = arr[i].strip()
            elif 'Horsepower' in label[i]:
                if 'unknown' not in arr[i].strip().lower():
                    item["other_specs_horse_power"] = arr[i].split('HP')[0].strip()
        yield item       
