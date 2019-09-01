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
from dateutil.relativedelta import relativedelta
from autodata.items import AutodataItem, MetaItem

class XcarsSpider(scrapy.Spider):
    name = 'xcars'
    allowed_domains = []
    start_urls = ["http://www.xcars.co/home"]

    def parse(self, response):
        number = response.xpath('//div[@class="ast_image"]/a/@href').extract()
        print(number)
        for n in number:
            yield Request(n, callback = self.parse_data, dont_filter = True)

    def parse_data(self, response):

        details = response.xpath('//div[@class="booking-info zxcv abcd"]')
        for det in details:
            
            item=AutodataItem()
            item2 = MetaItem()
            item["Last_Code_Update_Date"] = ""
            item["Scrapping_Date"] = ""
            item["Country"] = "KSA"
            item["City"] = ""
            item["Seller_Type"] = "Large Independent Dealers"
            item["Seller_Name"] = "Xcars"
            item["Car_URL"] = ""
            item["Car_Name"] = ""
            item["Year"] = ""
            item["Make"] = "".join(det.xpath('h2/span[1]/text()').extract()).strip()
            item["model"] = "".join(det.xpath('h2/span[2]/text()').extract()).strip()
            item["Spec"] = "".join(det.xpath('h2/span[2]/text()').extract()).strip()
            item["Car_Name"] = item["Make"] + ' ' + item["model"]
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
            item['Last_Code_Update_Date'] = 'Thursday, June 04, 2019'
            item['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
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

            for li in det.xpath('//div[@class="col-xs-7"]/ul/li'):
                key = ''.join(li.xpath('p[1]/text()').extract()).strip()
                value = ''.join(li.xpath('p[2]/text()').extract()).strip()
                if 'Price' in key:
                    item['Price_Currency'] = value.split(' ')[-1]
                    item['asking_price_inc_VAT'] = value.split(' ')[0]
                elif 'Year' in key:
                    item['Year'] = value
                elif 'Mileage' in key:
                    item['mileage'] = value.split(' ')[0]
                    item['mileage_unit'] = value.split(' ')[-1]
                elif 'Exterior' in key:
                    item["colour_exterior"] = value
                elif 'Interior' in key:
                    item["colour_interior"] = value

            item2['src'] = "xcars.co"
            item2['ts'] = datetime.utcnow().isoformat()
            item2['name'] = "xcars"
            item2['url'] = response.url
            item2['uid'] = str(uuid.uuid4())
            item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
            item['meta'] = dict(item2)
            item['Car_URL'] = response.url
            item['Source'] = item2['src']
            yield item
