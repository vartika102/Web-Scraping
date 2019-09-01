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
#from autodata.items import AutodataItem, MetaItem
from autodata.items import AutodataItem, MetaItem

class BmwAbuSpider(scrapy.Spider):
    name = "bmw_abu"
    allowed_domains = []
    urls = []
    start_urls = ["https://www.bmw-abudhabi.com/en_AE/local-content/pre-owened-vehicles/introduction/_jcr_content/par/iframeadaptive.integration-iframe.json"]

    def parse(self,response):
        body = json.loads(response.body)
        url = "https://bps.bmw.com/AE/en_AE/001860-dg"+"/search?q=%3Arelevance"
        yield Request(url,callback=self.parse_listings,meta={"url":url,"body":body})
        

    def parse_listings(self,response):
        url = response.meta["url"]
        body = response.meta["body"]
        sel = Selector(response)
        divs = sel.xpath('//div[@class="product__listing product__grid row"]/div')
        for div in divs:
            listing_url = "https://bps.bmw.com"+''.join(div.xpath('.//a[@class="thumb"]/@href').extract()).strip()
            yield Request(listing_url,callback=self.parse_data,meta={"url":url,"body":body})

    def parse_data(self,response):
        #item1 = AutodataItem()
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
        item1['vat'] = 'yess'
        item1['mileage_unit'] = ''
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
        item1['acceleration'] = ''
        item1['torque_Nm'] = ''

        sel = Selector(response)
        item1['Last_Code_Update_Date'] = 'Thursday, June 04, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
        item1["Car_URL"] = response.url
        item1["Country"] = "UAE"
        item1["City"] = "Dubai"
        item1["Make"] = "BMW"
        item1["Car_Name"] = "BMW " + ''.join(sel.xpath('//div[@class="col-flex pdp-details-top-title"]/h2/text()').extract()).strip()
        #item1["model"] = item1["Car_Name"].split(' ')[1]
        #item1["Spec"] = ' '.join(item1["Car_Name"].split(' ')[2:])
        item1["Price_Currency"] = ''.join(sel.xpath('//div[@class="pdp-details-top-info-price"]/h3/span//text()').extract()).strip().replace(u'\xa0', u' ').split(' ')[0]
        item1["asking_price_inc_VAT"] = ''.join(sel.xpath('//div[@class="pdp-details-top-info-price"]/h3/span//text()').extract()).strip().replace(u'\xa0', u' ').split(' ')[1]
        details_panels = sel.xpath('//div[@class="vehicle-details-panel"]/div[@class="vehicle-details-panel-feature"]')
        print(len(details_panels))
        for det in details_panels:
            name = ''.join(det.xpath('div[1]//text()').extract()).strip()
            value = ''.join(det.xpath('div[2]//text()').extract()).strip()
            #print(name)
            if  name.lower() == "model year":
                item1['Year'] = value
            elif name.lower() == "transmission":
                item1['transmission'] = value
            elif name.lower() == "basic paintwork":
                item1['colour_exterior'] = value
            elif name.lower() == "number of doors":
                item1['Doors'] = value
            elif name.lower() == "mileage":
                item1['mileage'] = value.replace(u'\xa0', u' ').split(' ')[0]
                item1['mileage_unit'] = value.replace(u'\xa0', u' ').split(' ')[1]
            elif name.lower() == "model":
                item1['model'] = value
            elif name.lower() == "body type":
                item1['bodystyle'] = value.replace('Coupé','Coupe')
            elif name.lower() == "fuel type":
                item1['fuel_type'] = value
            elif name.lower() == "engine power(hp)":
                item1['other_specs_horse_power'] = value.replace(u'\xa0', u' ').split(' ')[0]
            elif name.lower() == "number of seats":
                item1['other_specs_seats'] = value
            elif name.lower() == "upholstery type":
                item1['trim'] = value
            elif name.lower() == "warranty in months":
                item1['warranty_untill_when'] = (datetime.today() + relativedelta(months=+int(value))).strftime('%Y-%m-%d')
            elif name == "Number of Cylinders":
                item1['cylinders'] = value
            elif name.lower() == "cylinder capacity":
                item1['other_specs_engine_size'] = int(value.replace(u'\xa0', u' ').split(' ')[0])
                item1['engine_unit'] = 'cc'
                #item1['other_specs_engine_size'] = int(value.replace(u'\xa0', u' ').split(' ')[0]) * 0.001
            
        if item1['warranty_untill_when'] != "":
            item1['warranty'] = "yes"
        item1["Seller_Name"] = ''.join(sel.xpath('//p[@class="plan-route-map-container-dealer-info-name"]/text()').extract()).strip()
        item2['src'] = "bmw-dubai.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "bmw"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Source'] = item2['src']
        yield item1
        


