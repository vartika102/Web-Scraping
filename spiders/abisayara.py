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

class AbisayaraSpider(scrapy.Spider):
    name = 'abisayara'
    allowed_domains = []
    start_urls = ['https://www.abisayara.com/search/list?id_make=&id_model=&id_domicile=&qs_used=U&price_from=0&price_to=0&year_from=0&year_to=0&mileage_from=0&mileage_to=0&search=Search+5068++%E2%96%B6']
    #start_urls = ['https://www.abisayara.com/search/list?id_make=&id_model=&id_domicile=&price_from=0&price_to=0&year_from=0&year_to=0&mileage_from=0&mileage_to=0&search=Search+9430++%E2%96%B6']
    #start_urls = ['https://www.abisayara.com/search/list?page=2&id_domicile=&search=Search+5068++%E2%96%B6&id_make=&id_model=&sort=&type=desc&qs_new=&qs_used=U&mileage_to=0&mileage_from=0&price_to=0&price_from=0&year_to=0&year_from=0

    def parse(self,response):
        #cars = response.xpath('//div[@class="latest_left carsale cars_spc list_ad"]/ul/li')
        #print("###########",''.join(response.xpath('//div[@class="pagination"]/form/span[@class="nav_pagelink"][2]/a/text()').extract()).strip())
        total = int(''.join(response.xpath('//div[@class="pagination"]/form/span[@class="nav_pagelink"][2]/a/text()').extract()).strip())
        for i in range(total):
            url = 'https://www.abisayara.com/search/list?page=' + str(i+1) + '&id_domicile=&search=Search+5068++%E2%96%B6&id_make=&id_model=&sort=&type=desc&qs_new=&qs_used=U&mileage_to=0&mileage_from=0&price_to=0&price_from=0&year_to=0&year_from=0'
            yield Request(url, callback = self.parse_url, dont_filter = True)

    def parse_url(self, response):
        cars = response.xpath('//div[@class="latest_left carsale cars_spc list_ad"]/ul/li')
        for car in cars:
            urll = ''.join(car.xpath('.//div[@class="left_car"]/a/@href').extract()).strip().replace('/ar/','/en/')
            if urll != '':
                url = 'https://www.abisayara.com' + urll
                yield Request(url, callback = self.parse_data, dont_filter = True)

    def parse_data(self, response):
        item2 = MetaItem()
        item1 = AutodataItem()

        item1["Last_Code_Update_Date"] = ""
        item1["Scrapping_Date"] = ""
        item1["Country"] = "Saudi Arabia"
        item1["City"] = ""
        item1["Seller_Type"] = "Market Places"
        #item1["Seller_Name"] = ""
        item1["Seller_Name"] = "".join(response.xpath('//div[@class="seller_logo_main clearfix"]/text()').extract()).strip().split('-')[0].replace('Dealer:','').strip()
        item1["Seller_Name"] = re.sub('[^0-9a-zA-Z]+', ' ', item1["Seller_Name"]).strip()
        item1["Car_URL"] = response.url
        item1["Car_Name"] = ''.join(response.xpath('//h1[@class="vif_heading"]/text()').extract()).strip()
        item1["Year"] = ""
        item1["Make"] = ""
        item1["model"] = ""
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

        details = response.xpath('//div[@class="vif_info"]')
        item1['Price_Currency'] = 'SAR'
        item1['asking_price_inc_VAT'] = ''.join(details.xpath('h3/text()').extract()).strip().split('SAR')[0].strip()
        dets = details.xpath('ul/li')
        for det in dets:
            key = ''.join(det.xpath('text()').extract()).strip().split(':')[0]
            value = ''.join(det.xpath('text()').extract()).strip().split(':')[1].strip()
            #print(key, value)
            if key == 'Make':
                item1['Make'] = value
            elif key == 'Model':
                item1['model'] = value
            elif key == 'Year':
                item1['Year'] = value
            elif key == 'Mileage':
                item1['mileage'] = value.split(' ')[0]
                item1['mileage_unit'] = 'km'
            elif key == 'City':
                item1['City'] = value
            elif key == 'Color':
                item1['colour_exterior'] = value
            elif key == 'Engine size':
                item1['other_specs_engine_size'] = value
            elif key == 'Gearbox':
                item1['transmission'] = value

        item2['src'] = "www.abisayara.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "abisayara"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Last_Code_Update_Date'] = 'Tuesday, June 18, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
        item1['Source'] = item2['src']
        yield item1

        #print("Done")
