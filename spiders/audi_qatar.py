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
import os
from autodata.items import AutodataItem, MetaItem

class AudiSpider(scrapy.Spider):
    name = 'audi_qatar'
    allowed_domains = []
    start_urls = ['http://www.audiappoved.com/en/pre-owned/search#Qatar']

    def parse(self, response):
        yield Request(response.url,callback=self.parse_page,dont_filter = True)
        sel = Selector(response)
        nextt = sel.xpath('//div[@class="container-fluid search-results"]/div[@class="pagination-footer container"]')
        url1 = ''.join(nextt.xpath('a[@class="go-next col-md-2 col-xs-6 ar-center"]/@href').extract()).strip()
        url2 = "https://www.audiappoved.com" + url1
        if(url1 != ''):
            yield Request(url2,callback=self.parse,dont_filter = True)
        pass

    def parse_page(self, response):
        sel = Selector(response)
        divs = sel.xpath('//div[@class="container inner"]/div[@class="item card col-md-4 col-sm-6"]')
        for div in divs:
            url = "https://www.audiappoved.com" + ''.join(div.xpath('div[@class="details"]/a/@href').extract()).strip()
            yield Request(url, callback=self.parse_data, dont_filter = True)

    def parse_data(self, response):

        item2 = MetaItem()
        item1 = AutodataItem()

        sel = Selector(response)
        details3 = sel.xpath('//div[@class="dealership"]')
        city = (''.join(details3.xpath('div[@class="address"]/p/text()').extract()).strip()).split(',')
        item1['Country'] = city[len(city)-1][1:]
        if(item1['Country'] == 'QA'):

            item1["Last_Code_Update_Date"] = ""
            item1["Scrapping_Date"] = ""
            item1["Country"] = ""
            item1["City"] = ""
            item1["Seller_Type"] = ""
            item1["Seller_Name"] = ""
            item1["Car_URL"] = ""
            item1["Car_Name"] = ""
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

            
            
            item1['Car_URL'] = response.url
            item1['Make'] = "Audi"
            
            details1 = sel.xpath('//div[@id="vehicle_cta"]/div[1]')
            item1['Car_Name'] = ''.join(details1.xpath('div[@class="title"]/text()').extract()).strip()
            item1['model'] = item1['Car_Name'].split(' ')[0]
            item1['Price_Currency'] = (''.join(details1.xpath('div[@class="price"]/div[@class="cashprice"]/text()').extract()).strip())[:3]
            item1['asking_price_inc_VAT'] = (''.join(details1.xpath('div[@class="price"]/div[@class="cashprice"]/text()').extract()).strip())[4:]

            details2 = sel.xpath('//div[@class="specs"]/div[@class="item"]')
            for det in details2:
                spec_item = ''.join(det.xpath('div[@class="spec_item"]/text()').extract()).strip()
                spec_data = ''.join(det.xpath('div[@class="spec_data"]/text()').extract()).strip()
                if 'year' in spec_item.lower():
                    item1['Year'] = spec_data
                elif 'colour' in spec_item.lower():
                    item1['colour_exterior'] = spec_data
                elif 'transmission' in spec_item.lower():
                    item1['transmission'] = spec_data
                elif 'engine size' in spec_item.lower():
                    item1['other_specs_engine_size'] = spec_data[:-2]
                    item1['engine_unit'] = spec_data[-2:]
                elif 'mileage' in spec_item.lower():
                    item1['mileage'] = spec_data[:-2]
                    item1['mileage_unit'] = spec_data[-2:]
                elif 'fuel type' in spec_item.lower():
                    item1['fuel_type'] = spec_data
                elif 'bhp' in spec_item.lower():
                    item1['other_specs_horse_power'] = spec_data[:3]

            details3 = sel.xpath('//div[@class="dealership"]')
            item1['Seller_Name'] = ''.join(details3.xpath('div[@class="wrapper"]/h2/text()').extract()).strip()
            city = (''.join(details3.xpath('div[@class="address"]/p/text()').extract()).strip()).split(',')
            item1['City'] = city[len(city)-2]
            item1['Country'] = city[len(city)-1][1:]
            
            item2['src'] = "audiapproved.com"
            item2['ts'] = datetime.utcnow().isoformat()
            item2['name'] = "audi"
            item2['url'] = response.url
            item2['uid'] = str(uuid.uuid4())
            item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
            item1['meta'] = dict(item2)
            item1['Last_Code_Update_Date'] = 'June 6, 2019'
            item1['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')
            item1['Source'] = item2['src']
            yield item1
            

