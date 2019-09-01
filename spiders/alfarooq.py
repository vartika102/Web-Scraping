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

class AlfarooqSpider(scrapy.Spider):
    name = 'alfarooq'
    allowed_domains = []
    start_urls = ['https://alfarooqautomotive.com/']

    def parse(self, response):
        paths = response.xpath('//div[@class="carousel-slider3"]/div')
        for path in paths:
            url = ''.join(path.xpath('a/@href').extract()).strip()
            yield Request(url, callback = self.parse_data, dont_filter = True)
        #print('##########',len(path))

    def parse_data(self, response):
        item2 = MetaItem()
        item1 = AutodataItem()
        details = response.xpath('//table[@class="table"]')

        item1["Last_Code_Update_Date"] = ""
        item1["Scrapping_Date"] = ""
        item1["Country"] = "Oman"
        item1["City"] = "".join(response.xpath('//tr[@class="listing_category_location"]/td[2]/text()').extract()).strip().split(',')[0]
        item1["Seller_Type"] = "Large Independent Dealers"
        item1["Seller_Name"] = "Alfarooq Automotive"
        item1["Car_URL"] = response.url
        item1["Car_Name"] = ''.join(response.xpath('//div[@class="col-lg-9 col-md-9 col-sm-9 col-xs-12 xs-padding-none"]/h2/text()').extract()).strip()
        item1["Year"] = "".join(response.xpath('//tr[@class="listing_category_year"]/td[2]/text()').extract()).strip()
        item1["Make"] = "".join(response.xpath('//tr[@class="listing_category_make"]/td[2]/text()').extract()).strip()
        item1["model"] = ''.join(response.xpath('//tr[@class="listing_category_model"]/td[2]/text()').extract()).strip()
        item1["Spec"] = ""
        item1["Doors"] = ""
        item1["transmission"] = "".join(response.xpath('//tr[@class="listing_category_transmission"]/td[2]/text()').extract()).strip().split(' ')[-1]
        item1["trim"] = ""
        item1["bodystyle"] = "".join(response.xpath('//tr[@class="listing_category_body-style"]/td[2]/text()').extract()).strip()
        item1["other_specs_gearbox"] = ""
        item1["other_specs_seats"] = ""
        item1["other_specs_engine_size"] = "".join(response.xpath('//tr[@class="listing_category_engine"]/td[2]/text()').extract()).strip().split('L')[0]
        item1["other_specs_horse_power"] = ""
        item1["colour_exterior"] = "".join(response.xpath('//tr[@class="listing_category_exterior-color"]/td[2]/text()').extract()).strip()
        item1["colour_interior"] = "".join(response.xpath('//tr[@class="listing_category_interior-color"]/td[2]/text()').extract()).strip()
        item1["fuel_type"] = ""
        item1["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
        item1["mileage"] = "".join(response.xpath('//tr[@class="listing_category_mileage"]/td[2]/text()').extract()).strip()
        item1["condition"] = "".join(response.xpath('//tr[@class="listing_category_condition"]/td[2]/text()').extract()).strip()
        item1["warranty_untill_when"] = ""
        item1['service_contract_untill_when'] = ''
        item1['Price_Currency'] = 'OMR'
        item1['asking_price_inc_VAT'] = ''.join(response.xpath('//div[@class="col-lg-3 col-md-3 col-sm-3 text-right xs-padding-none"]/h2/text()').extract()).strip()
        item1['asking_price_ex_VAT'] = ''
        item1['warranty'] = ''
        item1['service_contract'] = ''
        item1['vat'] = 'yes'
        item1['mileage_unit'] = 'km'
        item1['engine_unit'] = 'L'
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

        item2['src'] = "alfarooqautomotive.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "alfarooq"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Last_Code_Update_Date'] = 'Tuesday, June 18, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
        item1['Source'] = item2['src']
        yield item1
