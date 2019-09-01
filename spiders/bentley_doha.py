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
#from bentley_doha.items import BentleyDohaItem, MetaItem
from autodata.items import AutodataItem, MetaItem
USER_AGENT = 'bentley_doha (+http://doha.bentleymotors.com/meia/en/stock)'


class BentleySpider(scrapy.Spider):
    name = 'bentley_doha'
    allowed_domains = []
    start_urls = ['https://doha.bentleymotors.com/meia/en/stock/']

    def parse(self, response):
        sel = Selector(response)
        path = sel.xpath('//*[@id="results"]/article')
        for p in path:
            url = "https://doha.bentleymotors.com" + ''.join(p.xpath('.//div[@class = "column block"]/a[@class="mdx-gtm-srp-open-vdp button btn-primary details"]/@href').extract()).strip()
            yield Request(url, callback = self.parse_data, )
        pass

    def parse_data(self, response):

        #item1 = BentleyDohaItem()
        item2 = MetaItem()
        item1 = AutodataItem()
        item1["Last_Code_Update_Date"] = ""
        item1["Scrapping_Date"] = ""
        item1["Country"] = ""
        item1["City"] = ""
        item1["Seller_Type"] = ""
        item1["Seller_Name"] = "Bentley Motors Muscat"
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
        item1['engine_unit'] = ''
        item1['mileage_unit'] = ''
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
        item1['wheel_size'] = ''
        item1['top_speed_kph'] = ''
        item1['cylinders'] = ''
        item1['acceleration'] = ''
        item1['torque_Nm'] = ''

        sel = Selector(response)

        item1["Car_URL"] = response.url
        item1["Car_Name"] = ' '.join(''.join(sel.xpath('//div[@class="vehicle-title column block"]/h1//text()').extract()).strip().split(' ')[2:])
        
        item1["Price_Currency"] = ''.join(sel.xpath('//div[@class="vehicle-prive column block"]/div//text()').extract()).strip()[-3:]
        item1["asking_price_inc_VAT"] = ''.join(sel.xpath('//div[@class="vehicle-prive column block"]/div//text()').extract()).strip()[:-4]
        lis = sel.xpath('//ul[@class="unstyle tiles-container-10 s-space-5 vertical-collapse"]/li')
        for l in lis:
            key = ''.join(l.xpath('div/div[@class="column s50 m50 l50 bold"]//text()').extract()).strip()
            item = ''.join(l.xpath('div/div[@class="column s50 m50 l50 vertical-top"]//text()').extract()).strip()
            if key.lower() == "body style":
                item1["bodystyle"] = item
            elif key.lower() == "paint colour":
                item1["colour_exterior"] = item
            elif key.lower() == "registration date":
                item1["Year"] = item.split('.')[-1]
            elif key.lower() == "mileage":
                item1["mileage"] = item[:-2]
                item1['mileage_unit'] = item[-2:]
            elif key.lower() == "transmission":
                item1["transmission"] = item
            elif key.lower() == "engine":
                item1["other_specs_engine_size"] = item.split(' ')[0]
                item1['engine_unit'] = item.split(' ')[1]
            elif key.lower() == "torque":
                item1['torque_Nm'] = item.split(' ')[0]
            elif "acceleration" in key.lower():
                item1['acceleration'] = item.split(' ')[0]
            elif "maximum speed" in key.lower():
                item1['top_speed_kph'] = item.split(' ')[0]
            elif key.lower() == "power":
                item1["other_specs_horse_power"] = int(item.replace(u'\xa0', u' ').split(' ')[0]) * 1.34102
               
        
        item1["Make"] = 'Bentley'
        if len(item1['Car_Name'].split()) > 2:
            item1["model"] = ' '.join(item1["Car_Name"].split(' ')[1:-1])
            item1['Spec'] = item1["Car_Name"].split(' ')[-1]
        else:
            item1["model"] = ' '.join(item1["Car_Name"].split(' ')[1:])
        
        item1["Country"] = "Qatar"
        item1["City"] = "Doha"
        
        item1['Last_Code_Update_Date'] = 'Thursday, June 04, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
        item2['src'] = "doha.bentleymotors.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "bentley"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Source'] = item2['src']

        yield item1
        
