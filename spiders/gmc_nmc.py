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

class GmcNmcSpider(scrapy.Spider):
    name = 'gmc_nmc'
    allowed_domains = []
    start_urls = ["http://gmc.nmc.com.bh/pre-owned-vehicles/"]

    def parse(self, response):       
        path = response.xpath('//*[@id="content-wrap"]/div[5]/div/div/div/div/div')      
        for url in path:
            url_details = url.xpath('.//div[@class ="button module view-vehicle small"]/a/@href').extract()
            url_det = ('http://gmc.nmc.com.bh'+ ''.join(url_details)).strip()
            yield Request (url_det,callback = self.parse_data,dont_filter=True)
    
    def parse_data(self,response):

        item=AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = ""
        item["City"] = ""
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "National Motor Company"
        item["Car_URL"] = ""
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
        item['warranty'] = 'yes'
        item['service_contract'] = ''
        item['vat'] = 'yes'
        item['mileage_unit'] = ''
        item['engine_unit'] = ''
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

        item2['src'] = "gmc.nmc.com.bh"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "gmc_nmc"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']
        path = Selector(response)

        item['Year'] = ''.join(path.xpath('//div[@class="cell reg-year"]/span[@class="value reg-year"]/text()').extract()).strip()
        
        item['other_specs_engine_size'] =''.join(path.xpath('//div[@class="cell engine-size"]/span[@class="value engine-size"]/text()').extract()).strip().split(' ')[0]
        item['engine_unit'] = ''.join(path.xpath('//div[@class="cell engine-size"]/span[@class="value engine-size"]/text()').extract()).strip().split(' ')[1]
        item['colour_exterior'] =''.join(path.xpath('//div[@class="cell colour"]/span[@class="value colour"]/text()').extract()).strip()
        item['bodystyle'] =''.join(path.xpath('//div[@class="cell bodystyle"]/span[@class="value bodystyle"]/text()').extract()).strip()
        item['mileage'] =''.join(path.xpath('//div[@class="cell mileage"]/span[@class="value mileage"]/text()').extract()).strip().split(' ')[0]
        item['mileage_unit'] = ''.join(path.xpath('//div[@class="cell mileage"]/span[@class="value mileage"]/text()').extract()).strip().split(' ')[1]
        item['model'] = ''.join(path.xpath('//div[@class="title module"]/h3/span[@class= "model"]//text()').extract()).strip()
        item['Year'] = ''.join(path.xpath('//div[@class="title module"]/h3/span[@class= "year"]//text()').extract()).strip()
        item['Make'] = ''.join(path.xpath('//div[@class="title module"]/h3/span[@class= "make"]//text()').extract()).strip()
        item['asking_price_inc_VAT'] = ''.join(path.xpath('//*[@id="content-wrap"]/div[2]/div/div[1]/div/div[2]/div/div/span[2]/text()').extract()).strip().split('BHD')[1]
        item['Price_Currency'] = 'BHD'
        item['fuel_type'] = ''.join(path.xpath('//div[@class="cell fuel-type"]/span[@class="value fuel-type"]/text()').extract()).strip()
        item['colour_interior'] = ''.join(path.xpath('//div[@class="cell interior-colour"]/span[@class="value interior-colour"]/text()').extract()).strip()
        item['transmission'] = ''.join(path.xpath('//div[@class="cell transmission"]/span[@class="value transmission"]/text()').extract()).strip()
        item['Doors'] = ''.join(path.xpath('//div[@class="cell doors"]/span[@class="value doors"]/text()').extract()).strip()
        item['Car_Name'] = item['Make'] + ' ' +item['model'] + ' ' +item['Year']
        item['warranty_untill_when'] = (datetime.today() + relativedelta(months=+24)).strftime('%Y-%m-%d')
        
        yield item
