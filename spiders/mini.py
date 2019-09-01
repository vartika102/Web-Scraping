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
from datetime import datetime
import os
#from alialghanim.items import AlialghanimItem
from autodata.items import AutodataItem, MetaItem


class MiniSpider(scrapy.Spider):
    name = "mini"
    allowed_domains = []
    urls = []
    start_urls = ["https://www.mini-ksa.com/en_SA/home/range/mini-3-door-hatch.html"]

    
    def parse(self,response):
        details = response.xpath('//div[@class="md-modelgroup-summary-option js-wizard-view-option"]')
        print(len(details))
        for det in details:
            item=AutodataItem()
            item2 = MetaItem()
            item["Last_Code_Update_Date"] = ""
            item["Scrapping_Date"] = ""
            item["Country"] = "KSA"
            item["City"] = ""
            item["Seller_Type"] = ""
            item["Seller_Name"] = ""
            item["Car_URL"] = response.url
            item["Year"] = ""
            item["Make"] = "Mini"
            item["model"] = "".join(det.xpath('.//span[@class="md-heading md-fixedtext"]/text()').extract()).strip()
            item["Spec"] = ""
            item["Car_Name"] = item['Make'] + ' ' + item["model"]
            item["Doors"] = ""
            item["transmission"] = "".join(det.xpath('.//dd[@class="md-modelgroup-summary-description-list-transmission px-md pb-md"]//text()').extract()).strip()
            item["trim"] = ""
            item["bodystyle"] = ""
            item["other_specs_gearbox"] = ""
            item["other_specs_seats"] = ""
            item["other_specs_engine_size"] = "".join(det.xpath('.//div[@class="ms-disclaimer-item-text"]/span[@class="text-value"]/text()').extract()).strip()
            item["other_specs_horse_power"] = int("".join(det.xpath('.//dd[@class="md-modelgroup-summary-description-list-power px-md pb-md"]//text()').extract()).strip().split(' ')[0]) * 1.34102
            item["colour_exterior"] = ""
            item["colour_interior"] = ""
            item["fuel_type"] = "".join(det.xpath('.//dd[@class="md-modelgroup-summary-description-list-fuelType px-md pb-md"]//text()').extract()).strip()
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
            item['engine_unit'] = 'l'
            item['Last_Code_Update_Date'] = 'June 15, 2019'
            item['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')
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

            item2['src'] = "mini-ksa.com"
            item2['ts'] = datetime.utcnow().isoformat()
            item2['name'] = "mini"
            item2['url'] = response.url
            item2['uid'] = str(uuid.uuid4())
            item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
            item['meta'] = dict(item2)
            item['Car_URL'] = response.url
            item['Source'] = item2['src']
            item['Last_Code_Update_Date'] = 'Sunday, July 7, 2019'
            item['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')

##            keys = det.xpath('.//dt[@class="px-md pt-md pb-sm"]/text()').extract()
##            values = det.xpath('.//dd[@class="md-modelgroup-summary-description-list-power px-md pb-md"]//text()').extract()
##            for k in range(len(keys)):
##                key = ''.join(keys[k]).strip()
##                value = ''.join(values[k]).strip()
##                if "Power" in key:
##                    item["other_specs_horse_power"] = int(value.split(' ')[0]) * 1.34102
##                elif "fuel type" in key:
##                    item["fuel_type"] = value
##                elif "transmission" in key:
##                    item["transmission"] = value

            yield item
                    
        #det = ''.join(response.xpath('//div[@class="ms-disclaimer-item pr-xs"]//span[@class="text-unit"]/text()').extract()).strip()
        #print(len(det))
        
