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

class DhofarSpider(scrapy.Spider):
    name = "dhofar"
    allowed_domains = []
    urls = []
    start_urls = ["http://www.dhofarautomotive.com/pre-owned"]
        
    def parse(self,response):
        for href in response.xpath("//div[contains(@class, 'carprice')]/a//@href"):
            url="http://www.dhofarautomotive.com"+href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self,response):
        item = AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = ""
        item["City"] = ""
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "Dhofar Automotive"
        item["Car_URL"] = response.url
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

        item['Last_Code_Update_Date'] = 'June 6, 2019'
        item['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')

        item2['src'] = "dhofarautomotive.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "dhofar"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Source'] = item2['src']

        item['asking_price_inc_VAT'] = response.xpath("//ul[contains(@class, 'omr1')]/li/span/text()").extract()[0]
        item['Price_Currency'] = 'OMR'
        item['Make'] = response.xpath("//ul[contains(@class, 'fist_sec')]/li/text()").extract()[0]
        item['model'] = response.xpath("//ul[contains(@class, 'fist_for')]/li/text()").extract()[0]
        item['Car_Name'] = item['Make'] + ' ' + item['model']
        item['Year'] = response.xpath("//ul[contains(@class, 'fist_sec')]/li/text()").extract()[1]
        item['colour_exterior'] = response.xpath("//ul[contains(@class, 'fist_sec')]/li/text()").extract()[2]
        item['transmission'] = response.xpath("//ul[contains(@class, 'fist_sec')]/li/text()").extract()[3]      
        item['mileage'] = response.xpath("//ul[contains(@class, 'fist_for')]/li/text()").extract()[1].strip()
        item['mileage_unit'] = 'km'
        item['Doors'] = response.xpath("//ul[contains(@class, 'fist_for')]/li/text()").extract()[2]
        item['bodystyle'] = response.xpath("//ul[contains(@class, 'fist_for')]/li/text()").extract()[3]
        
        yield item

