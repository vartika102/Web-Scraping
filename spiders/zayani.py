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
from autodata.items import AutodataItem, MetaItem

class ZayaniSpider(scrapy.Spider):
    name = "zayani"
    allowed_domains = []
    start_urls = ['https://www.al-zayani.com/guarantee/pre-owned-vehicles/']

    def parse(self, response):
        sel = Selector(response)
        cars = sel.xpath('//div[@class="listing module used-list standard-list"]/div/div')
        print(len(cars))
        for car in cars:
            details = ''.join(car.xpath('div/div/div/div[@class="span8"]/div[@class="layout-8 load ui-draggable"]/div[@class="span3"]/div[@class="button module view-vehicle"]/a/@href').extract()).strip()
            url = 'https://www.al-zayani.com' + details
            yield Request(url, callback = self.parse_data, dont_filter = True)
        nextt = ''.join(sel.xpath('//div[@class="pagination"]/div/ul[@class="pages"]/li[@class="btn-next"]/a/@href').extract()).strip()
        print(nextt)
        if nextt != '':
            url = 'https://www.al-zayani.com/guarantee/pre-owned-vehicles/' + nextt
            yield Request(url, callback = self.parse, dont_filter = True)

    def parse_data(self, response):

        sel = Selector(response)
        item2 = MetaItem()
        item1 = AutodataItem()

        item1["Last_Code_Update_Date"] = ""
        item1["Scrapping_Date"] = ""
        item1["Country"] = 'Syria'
        item1["City"] = ''.join(sel.xpath('//div[@class="location-address module"]/section/div/span[@class="address-city"]/text()').extract()).strip()
        item1["Seller_Type"] = "Large Independent Dealers"
        item1["Seller_Name"] = "Al-Zayani"
        item1["Car_URL"] = response.url
        item1["Year"] = ''.join(sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div/div[@class="cell reg-year"]/span[@class = "value reg-year"]/text()').extract()).strip()
        item1["Make"] = ''.join(sel.xpath('//div[@class="title module align-center"]/h3/span[@class="make"]/text()').extract()).strip()
        item1["model"] = ''.join(sel.xpath('//div[@class="title module align-center"]/h3/span[@class="model"]/text()').extract()).strip()
        item1["Spec"] = ''.join(sel.xpath('//div[@class="title module align-center"]/h3/span[@class="variant"]/text()').extract()).strip()
        item1["Car_Name"] = item1["Make"] + ' ' + item1["model"] + ' ' + item1["Spec"]
        item1["Doors"] = ""
        item1["transmission"] = ''.join(sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div/div[@class="cell transmission"]/span[@class = "value transmission"]/text()').extract()).strip()
        item1["trim"] = ""
        item1["bodystyle"] = ''.join(sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div/div[@class="cell bodystyle"]/span[@class = "value bodystyle"]/text()').extract()).strip()
        item1["other_specs_gearbox"] = ""
        item1["other_specs_seats"] = ""
        item1["other_specs_engine_size"] = ' '.join(''.join(sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div/div[@class="cell engine-size"]/span[@class = "value engine-size"]/text()').extract()).strip().split(' ')[:-1])
        item1["other_specs_horse_power"] = ""
        item1["colour_exterior"] = ''.join(sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div/div[@class="cell exterior-colour"]/span[@class = "value exterior-colour"]/text()').extract()).strip()
        item1["colour_interior"] = ""
        item1["fuel_type"] = ''.join(sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div/div[@class="cell fuel-type"]/span[@class = "value fuel-type"]/text()').extract()).strip()
        item1["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
        item1["mileage"] = ' '.join(''.join(sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div/div[@class="cell mileage"]/span[@class = "value mileage"]/text()').extract()).strip().split(' ')[:-1])
        item1["condition"] = ""
        item1["warranty_untill_when"] = ""
        item1['service_contract_untill_when'] = ''
        item1['Price_Currency'] = ''.join(sel.xpath('//div[@class="price-now"]/span[@class="value"]/text()').extract()).strip().split(' ')[0]
        item1['asking_price_inc_VAT'] = ''.join(sel.xpath('//div[@class="price-now"]/span[@class="value"]/text()').extract()).strip().split(' ')[1]
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
        item1['mileage_unit'] = ''.join(sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div/div[@class="cell mileage"]/span[@class = "value mileage"]/text()').extract()).strip().split(' ')[-1]
        item1['engine_unit'] = ''.join(sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div/div[@class="cell engine-size"]/span[@class = "value engine-size"]/text()').extract()).strip().split(' ')[-1]

        item2['src'] = "al-zayani.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "zayani"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Last_Code_Update_Date'] = 'June 13, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')
        item1['Source'] = item2['src']
        yield item1
