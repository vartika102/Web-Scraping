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

class MascarsSpider(scrapy.Spider):
    name = 'mascars'
    allowed_domains = []
    #start_urls = ['http://www.mascars.net/']
    start_urls = ['http://www.mascars.net/cars-search']

    def parse(self,response):
        #print("@@@@@")
        paths = response.xpath('//div[@class="main_container"]//div[@class="container"]/div/div[@class="search_result_data"]/div')
        for path in paths:
            url = 'http://www.mascars.net' + ''.join(path.xpath('.//div[@class="search_data"]/a[@class="search_data_details"]/@href').extract()).strip()
            yield Request(url, callback = self.parse_data, dont_filter = True)
        url = ''.join(response.xpath('.//div[@class="item-list"]//li[@class="pager-next"]/a/@href').extract()).strip()
        next_url = 'http://www.mascars.net' + url
        if url != '':
            #print("Trueeeeeeee")
            yield Request(next_url, callback = self.parse, dont_filter = True)

    def parse_data(self, response):
        item2 = MetaItem()
        item1 = AutodataItem()

        item1["Last_Code_Update_Date"] = ""
        item1["Scrapping_Date"] = ""
        item1["Country"] = "Saudi Arabia"
        item1["City"] = ""
        item1["Seller_Type"] = "Large Independent Dealers"
        item1["Seller_Name"] = "Mas Cars"
        item1["Car_URL"] = response.url
        item1["Car_Name"] = ''.join(response.xpath('//span[@class="inner-nice-model-title"]/text()').extract()).strip()
        item1["Year"] = ""
        item1["Make"] = ""
        item1["model"] = ''.join(response.xpath('//div[@class="internal_details"]//ul//span[@id = "get-my-model"]/text()').extract()).strip()
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

        item1["Make"] = ''.join(response.xpath('//div[@class="internal_details"]//ul//span[@id = "get-my-manufac"]/text()').extract()).strip()
        details = response.xpath('//div[@class="internal_details"]//ul/li')
        for det in details:
            key = ''.join(det.xpath('strong[1]/text()').extract()).strip()
            value = ''.join(det.xpath('span[1]/text()').extract()).strip()
            if key == "Year:":
                item1['Year'] = value
            elif key == "Car Color:":
                item1["colour_exterior"] = value
            elif key == "Internal Color:":
                item1["colour_interior"] = value
            elif key == "Transmission:":
                item1["transmission"] = value
            elif key == "Engine:":
                item1["mileage"] = value
                item1["mileage_unit"] = 'km'
            elif key == "Price:":
                item1["asking_price_inc_VAT"] = value.split(' ')[0]
                item1["Price_Currency"] = value.split(' ')[1]
            elif key == "Warrenty:":
                item1["warranty"] = value
##            elif key == "Type:":
##                item1["colour_exterior"] = value
        item1["Car_Name"] = item1['Make'] + ' ' + item1['model']
        
        item2['src'] = "www.mascars.net"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "mascars"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Last_Code_Update_Date'] = 'Tuesday, June 18, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
        #item1['Seller_Name'] = 'Universal Motors Agencies'
        item1['Source'] = item2['src']
        yield item1

        #print("####")
