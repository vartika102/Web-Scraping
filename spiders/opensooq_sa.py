# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
import requests
import json
import re
import uuid
import hashlib
import logging
import subprocess
from datetime import datetime,date
from autodata.items import AutodataItem, MetaItem

class OpensooqSaSpider(scrapy.Spider):
    name = 'opensooq_sa'
    allowed_domains = []
    start_urls = ['https://sa.opensooq.com/en/cars/cars-for-sale']

    def parse(self,response):
        cars = response.xpath('//div[@class="post-item"]/ul/li[@class="rectLi ie relative mb15"]//h2[@class="fRight mb15"]')
        for car in cars:
            url = 'https://sa.opensooq.com' + ''.join(car.xpath('a/@href').extract()).strip()
            yield Request(url, callback = self.parse_data, dont_filter = True)
        url = ''.join(response.xpath('//ul[@class = "pagination"]/li[@class="next"]/a/@href').extract()).strip()
        next_url = 'https://sa.opensooq.com' + url
        if url != '':
            yield Request(next_url, callback = self.parse, dont_filter = True)

    def parse_data(self, response):
        print("done")
        item2 = MetaItem()
        item1 = AutodataItem()

        item1["Last_Code_Update_Date"] = ""
        item1["Scrapping_Date"] = ""
        item1["Country"] = "Saudi Arabia"
        item1["City"] = ""
        item1["Seller_Type"] = "Market Places"
        item1["Seller_Name"] = "Opensooq"
        item1["Car_URL"] = response.url
        item1["Car_Name"] = ''
        item1["Year"] = ""
        item1["Make"] = ""
        item1["model"] = ''
        item1["Spec"] = ""
        item1["Doors"] = ""
        item1["transmission"] = ""
        item1["trim"] = ""
        item1["bodystyle"] = ""
        item1["other_specs_gearbox"] = ""
        item1["other_specs_seats"] = ""
        item1["other_specs_engine_size"] = ""
        item1["other_specs_horse_power"] = ""
        item1["colour_exterior"] = ""
        item1["colour_interior"] = ""
        item1["fuel_type"] = ""
        item1["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
        item1["mileage"] = ""
        item1["condition"] = ""
        item1["warranty_untill_when"] = ""
        item1['service_contract_untill_when'] = ''
        item1['Price_Currency'] = ''
        item1['asking_price_inc_VAT'] = ''
        item1['asking_price_ex_VAT'] = ''
        item1['warranty'] = ''
        item1['service_contract'] = ''
        item1['vat'] = 'yes'
        item1['mileage_unit'] = ''
        item1['engine_unit'] = ''
        item1['autodata_Make'] = ''
        item1['autodata_Make_id'] = ''
        item1['autodata_model'] = ''
        item1['autodata_model_id'] = ''
        item1['autodata_Spec'] = ''
        item1['autodata_Spec_id'] = ''
        item1['autodata_transmission'] = ''
        item1['autodata_transmission_id'] = ''
        item1['autodata_bodystyle'] = ''
        item1['autodata_bodystyle_id'] = ''

        details = response.xpath('//div[@class="customP"]/ul/li')
        for det in details:
            key = ''.join(det.xpath('span/text()').extract()).strip()
            value = ''.join(det.xpath('a/text()').extract()).replace('\"','').strip()
            #print(key, value)
            if 'city' in key.lower():
                item1["City"] = value
            elif 'make' in key.lower():
                item1["Make"] = value
            elif 'model' in key.lower():
                item1["model"] = value
            elif 'year' in key.lower():
                item1["Year"] = value
            elif 'condition' in key.lower():
                item1["condition"] = value
            elif 'kilometers' in key.lower():
                item1["mileage"] = value.split(' ')[0].replace('+','')
            elif 'transmission' in key.lower():
                item1["transmission"] = value
            elif 'fuel' in key.lower():
                item1["fuel_type"] = value
            elif 'color' in key.lower():
                item1["colour_exterior"] = value
            elif 'price' in key.lower():
                item1["Price_Currency"] = value
                item1['asking_price_inc_VAT'] = ''.join(det.xpath('a/strong/text()').extract()).strip()

        item1["Car_Name"] = item1["Make"] + ' ' + item1["model"]
        item2['src'] = "sa.opensooq.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "opensooq_sa"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Last_Code_Update_Date'] = 'Tuesday, June 18, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
        item1['Source'] = item2['src']
        if item1['Car_Name'] != '':
            yield item1
