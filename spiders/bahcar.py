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
from dateutil.relativedelta import relativedelta
import os
from autodata.items import AutodataItem, MetaItem

class BahcarSpider(scrapy.Spider):
    name = "bahcar"
    allowed_domains = []
    urls = []
    start_urls = ["https://www.bahcar.com/used-cars/2/1/"]
    
    def parse(self, response):
        divs = response.xpath('//div[@class="h_usedcars carlist_usedcars clearfix"]/div')
        print(len(divs))
        for div in divs:
            new_url = ''.join(div.xpath('.//h3[@class="item-name"]/a/@href').extract()).strip()
            if new_url != 'javascript:void(0)':
                yield Request(new_url, callback = self.parse_data, dont_filter = True)
            else:
                print(new_url)
        path = response.xpath('//div[@class="col-lg-8 col-sm-12 col-xs-12"]//ul[@class="pagination"]/li')
        for li in path:
            url = ''.join(li.xpath('a/@href').extract()).strip()
        if url != '':
            yield Request(url, callback = self.parse, dont_filter = True)
        pass

    def parse_data(self, response):
        item=AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "Bahrain"
        item["City"] = ""
        item["Seller_Type"] = "Market Places"
        item["Seller_Name"] = "Bahrain Cars"
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
        item['mileage_unit'] = 'km'
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

        item2['src'] = "www.bahcar.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "bahcar"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']

        details = response.xpath('//div[@class="info"]')
        for det in details:
            key = ''.join(det.xpath('a/h3/text()').extract()).strip()
            value = ''.join(det.xpath('p/text()').extract()).strip()
            if 'ask' in value.lower():
                continue
            elif 'Make' in key:
                item['Make'] = value
            elif 'Trim' in key:
                item['model'] = value
            elif 'Year' in key:
                item['Year'] = value
            elif 'Price' in key:
                item['Price_Currency'] = value.split(' ')[0]
                item['asking_price_inc_VAT'] = value.split(' ')[-1]
                if 'BD' in item['asking_price_inc_VAT']:
                    item['asking_price_inc_VAT'] = ''
            elif 'Kilometer' in key:
                item['mileage'] = value
            elif 'Transmission' in key:
                item['transmission'] = value
            elif 'Body Style' in key:
                item['bodystyle'] = value
            elif 'Exterior Color' in key:
                item['colour_exterior'] = value
            elif 'Interior Color' in key:
                item['colour_interior'] = value
        item["Car_Name"] = item['Make'] + ' ' + item['model']
        yield item

        pass
