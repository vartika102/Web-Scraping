# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
from scrapy.linkextractors import LinkExtractor
import requests
import json
import re
import uuid
import hashlib
import logging
import subprocess
import json
from datetime import datetime,date
from autodata.items import AutodataItem, MetaItem

class MaseratiSpider(scrapy.Spider):
    name = 'maserati'
    allowed_domains = []
    start_urls = ['https://ws.maserati.com/comserv/public/stl/searchByFilter?country=171&language=en&searchType=preowned&nPageElement=12&nPage=1&dealerCode=63653&bodyStyle=GH%7CLV%7CQP%7CGT%7CGC%7CQPOLD%7CGS%7CGSS%7CSP%7CCP%7CCLA&mileageFROM=0&mileageTO=1000000&modelYearFROM=2000&modelYearTO=2030&priceFROM=0&priceTO=10000000&sortField=price&sortType=asc&geoLat=NaN&geoLong=NaN&callback=jp_y8qgufc6yu_5']
    
    def parse(self, response):
        data1 = str(response.body)
        data2 = data1[data1.index('{'):-3]
        json_acceptable_string = data2.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        number = str(d['result']['records'])
        url = 'https://ws.maserati.com/comserv/public/stl/searchByFilter?country=171&language=en&searchType=preowned&nPageElement=' + number + '&nPage=1&dealerCode=63653&bodyStyle=GH%7CLV%7CQP%7CGT%7CGC%7CQPOLD%7CGS%7CGSS%7CSP%7CCP%7CCLA&mileageFROM=0&mileageTO=1000000&modelYearFROM=2000&modelYearTO=2030&priceFROM=0&priceTO=10000000&sortField=price&sortType=asc&geoLat=NaN&geoLong=NaN&callback=jp_y8qgufc6yu_5'
        yield Request(url, callback = self.parse_data, dont_filter = True)

    def parse_data(self, response):
        data1 = str(response.body)
        data2 = data1[data1.index('{'):-3]
        json_acceptable_string = data2.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        rows  = d['result']['rows']
        for row in rows:
            item2 = MetaItem()
            item1 = AutodataItem()

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
            item1['vat'] = ''
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

            item1['model'] = row['modelName']
            item1['Year'] = str(row['modelYear'])
            item1['mileage'] = row['mileage'].split(' ')[0]
            item1['mileage_unit'] = row['mileage'].split(' ')[1]
            item1['other_specs_horse_power'] = int(row['maxPowerKw'].split(' ')[0]) * 1.34102
            item1['Seller_Name'] = row['dealer']['name']
            item1['Country'] = row['dealer']['country']
            item1['City'] = row['dealer']['city']
            item1['asking_price_inc_VAT'] = row['price']
            item1['Price_Currency'] = row['formattedPrice'].split(' ')[0]
            item1['bodystyle'] = row['bodyStyle']
            item1["colour_exterior"] = row['exterior']
            item1["colour_interior"] = row['interior']
            item1['Last_Code_Update_Date'] = 'June 6, 2019'
            item1['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')
            item1['Make'] = 'Maserati'
            item1['vat'] = 'yes'
            item1["Car_URL"] = response.url
            item1["Car_Name"] = "Maserati" + ' ' + item1['model']
            item2['src'] = "maserati.com"
            item2['ts'] = datetime.utcnow().isoformat()
            item2['name'] = "maserati"
            item2['url'] = response.url
            item2['uid'] = str(uuid.uuid4())
            item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
            item1['meta'] = dict(item2)
            item1['Source'] = item2['src']
            yield item1

        pass
