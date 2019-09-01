# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
from scrapy.linkextractors import LinkExtractor
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
from datetime import datetime, date
import os
from dateutil.relativedelta import relativedelta
from autodata.items import AutodataItem, MetaItem
count = 0
class BmwSaSpider(scrapy.Spider):
    name = "bmw_sa"
    allowed_domains = []
    urls = []
    count = 0
    start_urls = ["https://retailcomponent.salescre8.com/v1/services/retail-component/publications/search?channelId=www_bmwsa&childQuery=&locale=en_GB&parentQuery=&profile=bmw&rows=20&sort=&sortOrder=&start=0"]

    def parse(self,response):
        body = json.loads(response.body)
        data = body['results']
        print(len(data))

        for res in data:            
            item2 = MetaItem()
            item1 = AutodataItem()
            item1["Last_Code_Update_Date"] = ""
            item1["Scrapping_Date"] = ""
            item1["trim"] = ''
            item1["Country"] = "Saudi Arabia"
            item1["City"] = res['vehicle']['location']['city']
            item1["Seller_Type"] = "Official Dealers"
            item1["Seller_Name"] = "Mohamed Yousuf Naghi - BMW"
            item1["Car_URL"] = ""
            item1["bodystyle"] = res['vehicle']['bodyType']['pl_PL']
            item1["Car_Name"] = ""
            item1["Year"] = str(res['vehicle']['constructionYear'])
            item1["Make"] = res['vehicle']['make']
            item1["Doors"] = ""
            item1["transmission"] = res['vehicle']['transmission']['key'].split('.')[1]
            if 'seatFabric' in res['vehicle']:
                item1["trim"] = res['vehicle']['seatFabric']['key'].split('.')[1]
            item1["model"] = res['vehicle']['model'].replace(item1['bodystyle'],'')
            item1["Spec"] = res['vehicle']['vehicleVersion'].split('-')[0].replace(item1['bodystyle'],'').strip()
            item1["other_specs_gearbox"] = ""
            item1["other_specs_seats"] = ""
            item1["other_specs_engine_size"] = ""
            item1["other_specs_horse_power"] = res['vehicle']['power_hp']
            item1["colour_exterior"] = res['vehicle']['bodyColor']['key'].split('.')[1]
            item1["colour_interior"] = res['vehicle']['interiorColor']['key'].split('.')[1]
            item1["fuel_type"] = res['vehicle']['fuel']['key'].split('.')[1]
            item1["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
            item1["mileage"] = res['vehicle']['mileage_km']
            item1["condition"] = ""
            item1["warranty_untill_when"] = ""
            item1['service_contract_untill_when'] = ''
            item1['Price_Currency'] = res["retailpricing"]["applicableCurrency"]
            item1['asking_price_inc_VAT'] = res['priceInclusiveVAT']
            item1['asking_price_ex_VAT'] = res['priceExclusiveVAT']
            item1['warranty'] = ''
            item1['service_contract'] = ''
            item1['vat'] = 'yes'
            item1['mileage_unit'] = 'km'
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
            item1['wheel_size'] = ''
            item1['top_speed_kph'] = ''
            item1['cylinders'] = ''
            if 'numberOfCylinders' in res['vehicle']:
                item1['cylinders'] = res['vehicle']['numberOfCylinders']
            item1['acceleration'] = ''
            item1['torque_Nm'] = ''
            item1['Last_Code_Update_Date'] = 'Wednesday, July 03, 2019'
            item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
            item1["Car_URL"] = response.url
            item1["Car_Name"] = item1["Make"] + ' ' + item1["model"] + item1["Spec"]

            item2['src'] = "bmw-saudiarabia.com"
            item2['ts'] = datetime.utcnow().isoformat()
            item2['name'] = "bmw_sa"
            item2['url'] = response.url
            item2['uid'] = str(uuid.uuid4())
            item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
            item1['meta'] = dict(item2)
            item1['Source'] = item2['src']

            yield item1
        
        count = int(response.url.split('start=')[1]) + 20
        if len(data) != 0:
            url = "https://retailcomponent.salescre8.com/v1/services/retail-component/publications/search?channelId=www_bmwsa&childQuery=&locale=en_GB&parentQuery=&profile=bmw&rows=20&sort=&sortOrder=&start="+ str(count)
            yield Request(url,callback=self.parse,meta={"url":url,"body":body})
