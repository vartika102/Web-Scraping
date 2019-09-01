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
#from aljazirah.items import AljazirahItem
from autodata.items import AutodataItem, MetaItem

class AljazirahSpider(scrapy.Spider):
    name = "aljazirah"
    allowed_domains = []
    urls = []
    start_urls = ["https://en.aljazirahford.com/Vehicles/Search?Condition=2&friendlyURL=used-cars-aljazirah-vehicles-agencies-saudi-arabia"]
    
    def parse(self, response):
        yield Request(response.url,callback=self.parse1,dont_filter = True)
        next = response.xpath("//ul[contains(@class,'pagelist')]/a[contains(@class,'pagination-page gruxIcon gw-grux-right01 highlightarrow')]//@href").get()
        
        if next is not None:
            nextt ="https://en.aljazirahford.com"+next
            yield Request(nextt,callback=self.parse,dont_filter = True)
        pass
    
    
    def parse1(self,response):
        for href in response.xpath("//div[contains(@class,'gw_stockList__vehicle__buttons')]/a//@href"):
            url="https://en.aljazirahford.com"+href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
    
    
    def parse_dir_contents(self,response):
        item=AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = ""
        item["City"] = ""
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "Al Jazirah Vehicle Agencies Co"
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
        item['warranty'] = ''
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

        item2['src'] = "en.aljazirahford.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "aljazirah"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']
        
        #       getting make
        item['asking_price_inc_VAT'] = response.xpath("//div[contains(@class, 'stockDetBluePrice')]/span/text()").get().split('SAR')[-1]

        item['Price_Currency'] = 'SAR'
        item['vat'] = 'yes'
        item['Make'] = response.xpath("//tr/td[contains(@property, 'manufacturer')]/text()").get()

        item['model'] = response.xpath("//tr/td[contains(@property, 'model')]/text()").get()
        item['Car_Name'] = item['Make'] + ' ' +item['model']
        item['Car_URL'] = response.url
        spec = response.xpath("//tr/td[contains(@property, 'name')]/text()").extract()
        if spec:
            item['Spec'] = spec[0].replace(',','')
        item['Year'] = response.xpath("//tr/td[contains(@property, 'dateVehicleFirstRegistered')]/text()").get()
        #item['Doors'] =
        #item['trim'] =

        #item['other_specs_gearbox'] =
        #item['other_specs_seats'] =
        item['fuel_type'] = response.xpath("//tr/td[contains(@property, 'fuelType')]/text()").get()
        item['transmission'] = response.xpath("//tr/td[contains(@property, 'vehicleTransmission')]/text()").get()
        
        item['mileage'] = response.xpath("//tr/td[contains(@property, 'mileageFromOdometer')]/text()").get().split('KM')[0].strip()
        item['mileage_unit'] = 'km'
        #item['other_specs_engine_size'] =

        
        #item['engine_unit'] = 'l'
        item['colour_exterior'] = response.xpath("//tr/td[contains(@property, 'color')]/text()").get()
        #item['colour_interior'] =
        #item['other_specs_horse_power'] =
        
        #item['bodystyle'] =
        
        yield item



    

