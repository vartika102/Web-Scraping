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
#from cadillac.items import CadillacItem
from autodata.items import AutodataItem, MetaItem

class CadillacMannaiautosSpider(scrapy.Spider):
    name = "cadillac_mannaiautos"
    allowed_domains = []
    urls = []
    start_urls = ["https://cadillac.mannaiautos.com/pre-owned-vehicles/"]
    
    
    
    def parse(self,response):
        for href in response.xpath("//div[contains(@class, 'title module')]/h3/a//@href"):
            url="https://cadillac.mannaiautos.com"+href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
    
    
    def parse_dir_contents(self,response):
        #item = CadillacItem()
        
        #item2 = MetaItem()
        #       getting make
        
        item2 = MetaItem()
        item = AutodataItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "Qatar"
        item["City"] = ""
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "Cadillac Mannai Autos"
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

        item2['src'] = "cadillac.mannaiautos.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "cadillac_mannaiautos"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Source'] = item2['src']
        
        item['asking_price_inc_VAT'] = (response.xpath("//div[contains(@class,'price-now')]/span[contains(@class,'value')]/text()").extract()[0]).split('QAR')[-1].strip()
        item['Price_Currency'] = 'QAR'
        item['Year'] = response.xpath("//div[contains(@class, 'title module align-center overview-title')]/h3/span[contains(@class, 'year')]/text()").extract()[0].strip()
        item['Make'] = response.xpath("//div[contains(@class, 'title module align-center overview-title')]/h3/span[contains(@class, 'make')]/text()").extract()[0].strip()
        item['model'] = response.xpath("//div[contains(@class, 'title module align-center overview-title')]/h3/span[contains(@class, 'model')]/text()").extract()[0].strip()
        item['Spec'] = response.xpath("//div[contains(@class, 'title module align-center overview-title')]/h3/span[contains(@class, 'variant')]/text()").extract()[0].strip()
        item['Car_Name'] = item['Make'] + ' ' + item['model'] + ' ' + item['Spec']
        item['transmission'] = response.xpath("//div[contains(@class, 'cell transmission')]/span[contains(@class, 'value transmission')]/text()").extract()[0].strip()
        item['bodystyle'] = response.xpath("//div[contains(@class, 'cell bodystyle')]/span[contains(@class, 'value bodystyle')]/text()").extract()[0].strip()
        item['mileage'] = ((response.xpath("//div[contains(@class, 'cell mileage')]/span[contains(@class, 'value mileage')]/text()").extract()[0]).split('miles')[0]).strip()
        item['mileage_unit'] = 'miles'
        item['other_specs_engine_size'] = ((response.xpath("//div[contains(@class, 'cell engine-size')]/span[contains(@class, 'value engine-size')]/text()").extract()[0]).split('l')[0]).strip()
        item['engine_unit'] = 'litre'
        item['colour_exterior'] = response.xpath("//div[contains(@class, 'cell colour')]/span[contains(@class, 'value colour')]/text()").extract()[0].strip()
        item['fuel_type'] = response.xpath("//div[contains(@class, 'cell fuel-type')]/span[contains(@class, 'value fuel-type')]/text()").extract()[0].strip()
        item['Doors'] = response.xpath("//div[contains(@class, 'cell doors')]/span[contains(@class, 'value doors')]/text()").extract()[0].strip()
        item['colour_interior'] = response.xpath("//div[contains(@class, 'cell interior-colour')]/span[contains(@class, 'value interior-colour')]/text()").extract()[0].strip()
        #item['PREVIOUS_OWNERS']=response.xpath("//div[contains(@class, 'cell previous-owners')]/span[contains(@class, 'value previous-owners')]/text()").extract()[0].strip()
        item['other_specs_seats'] = response.xpath("//div[contains(@class, 'cell num-seats')]/span[contains(@class, 'value num-seats')]/text()").extract()[0].strip()
        #item['Stock_No']=response.xpath("//div[contains(@class, 'cell stock-no')]/span[contains(@class, 'value stock-no')]/text()").extract()[0].strip()
        #item['ADDITIONAL_INFO']=response.xpath("//div[contains(@class, 'inner')]/div[contains(@class,'description-text')]/text()").extract()[0].strip()
        #item2['src'] = "cadillac.mannaiautos.com"
        #item2['ts'] = datetime.datetime.utcnow().isoformat()
        #item2['name'] = "cadillac"
        #item2['url'] = url
        #item2['uid'] = str(uuid.uuid4())
        #item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True)).hexdigest()
        
        #extras=response.xpath("//div[contains(@class, 'extras')]/p/text()").extract()
        #n=len(extras)
        
        #for i in range(0,n):
        #   a=extras[i]
        #   item['ADDITIONAL_INFO'].append(a)

        
        
        yield item



