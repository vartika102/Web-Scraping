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

class FourSpider(scrapy.Spider):
    name = "four"
    allowed_domains = []
    urls = []
    start_urls = ["https://www.4x4motors.com/"]
        
    def parse(self, response):
        last_page = response.xpath("//span[contains(@class,'total_pages')]/text()").get()
        last = int(last_page)
        for i in range(1, last+1):
            pages = str.join('',('https://www.4x4motors.com/?listing_order=date&listing_orderby=DESC&paged=',str(i)))
            yield(scrapy.Request(pages, callback=self.parse1))

    def parse1(self, response):
        for href in response.xpath("//a[contains(@class,'inventory has_badge')]//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item2 = MetaItem()
        item = AutodataItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = ""
        item["City"] = ""
        item["Seller_Type"] = ""
        item["Seller_Name"] = ""
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

        item2['src'] = "4x4motors.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "four"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Source'] = item2['src']
                
        item['Last_Code_Update_Date'] = 'Thursday,June 20,2019'
        item['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
        item['City'] = response.xpath("//tr[contains(@class,'listing_category_location')]/td/text()").extract()[-1]
        item["Country"] = "UAE"
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "4x4 Motors LLC"
        item["Car_URL"] = response.url
        item['Make'] = response.xpath("//tr[contains(@class,'listing_category_make')]/td/text()").extract()[-1]
        item['model'] = response.xpath("//tr[contains(@class,'listing_category_model')]/td/text()").extract()[-1]
        item['Car_Name'] = item['Make']+' '+item['model']
        item['Year'] = response.xpath("//tr[contains(@class,'listing_category_year')]/td/text()").extract()[-1]
        item['bodystyle'] = response.xpath("//tr[contains(@class,'listing_category_body-style')]/td/text()").extract()[-1]
        item['warranty_untill_when'] = (response.xpath("//tr[contains(@class,'listing_category_warranty')]/td/text()").extract()[-1].split('DEALER')[0]).strip()
        item['asking_price_inc_VAT'] = response.xpath("//tr[contains(@class,'listing_category_price')]/td/text()").extract()[-1].split('AED')[-1].strip()
        item['Price_Currency'] = "AED"
        item['colour_exterior']= response.xpath("//tr[contains(@class,'listing_category_exterior-color')]/td/text()").extract()[-1]
        item['transmission']= response.xpath("//tr[contains(@class,'listing_category_transmission')]/td/text()").extract()[-1]
        item['mileage']= response.xpath("//tr[contains(@class,'listing_category_kilometers')]/td/text()").extract()[-1]
        item['mileage_unit'] = 'km'
        yield item
