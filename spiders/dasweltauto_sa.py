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

class DasweltautoSaSpider(scrapy.Spider):
    name = "dasweltauto_sa"
    allowed_domains = []
    urls = []
    start_urls = ["http://www.dasweltauto.me/en/pre-owned/search#Saudi%20Arabia"]
       
    def parse(self, response):
        last_page = response.xpath("//div[contains(@class,'curr-page col-md-8 hidden-sm hidden-xs')]//text()").extract()[0]
        last = int(last_page.split('of')[-1])
        print("###########",last)
        for i in range(1, last+1):
            pages = str.join('',('http://www.dasweltauto.me/en/pre-owned/search?page=',str(i),'#Saudi%20Arabia'))
            yield(scrapy.Request(pages, callback=self.parse1))

    def parse1(self, response):
        for href in response.xpath("//a[contains(@class,'button tell-me-more')]//@href"):
            url="http://www.dasweltauto.me"+href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item2 = MetaItem()
        item = AutodataItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "Saudi Arabia"
        item["City"] = ""
        item["Seller_Type"] = "Large Independent Dealers"
        item["Seller_Name"] = "Dasweltauto"
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
        item['wheel_size'] = ''
        item['top_speed_kph'] = ''
        item['cylinders'] = ''
        item['acceleration'] = ''
        item['torque_Nm'] = ''

        item['Last_Code_Update_Date'] = 'Thursday, June 04, 2019'
        item['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
        item2['src'] = "dasweltauto.me"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "dasweltauto_sa"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Source'] = item2['src']

        dealer = response.xpath("//div[contains(@class,'dealership')]/div[contains(@class,'address')]/p/text()").get()
        if "SA" in dealer:

            item['Make'] = 'Volkswagen'
            item['Car_Name'] = item['Make'] + ' ' + response.xpath("//div[contains(@id,'vehicle_cta')]/div/div[contains(@class,'title')]/text()").extract()[0]
            item['Year']=response.xpath("//div[contains(@class,'item')]/div[contains(@class,'spec_data')]/text()").extract()[0]
            item['asking_price_inc_VAT']=((response.xpath("//div[contains(@class,'price')]/div[contains(@class,'cashprice')]/text()").extract()[0]).split('USD')[-1]).strip()
            item['Price_Currency'] = 'SAR'
            item['colour_exterior']=response.xpath("//div[contains(@class,'item')]/div[contains(@class,'spec_data')]/text()").extract()[1]
            item['transmission']=response.xpath("//div[contains(@class,'item')]/div[contains(@class,'spec_data')]/text()").extract()[2].strip()
            item['other_specs_engine_size']=((response.xpath("//div[contains(@class,'item')]/div[contains(@class,'spec_data')]/text()").extract()[3]).split('cc')[0]).strip()
            item['engine_unit'] = 'cc'
            item['mileage']=((response.xpath("//div[contains(@class,'item')]/div[contains(@class,'spec_data')]/text()").extract()[4]).split('km')[0]).strip()
            item['mileage_unit'] = 'km'
            item['acceleration'] = ((response.xpath("//div[contains(@class,'item')]/div[contains(@class,'spec_data')]/text()").extract()[6]).split(' ')[0]).strip()
            item['fuel_type']=response.xpath("//div[contains(@class,'item')]/div[contains(@class,'spec_data')]/text()").extract()[5]
            item['other_specs_horse_power']=((response.xpath("//div[contains(@class,'item')]/div[contains(@class,'spec_data')]/text()").extract()[7]).split('bhp')[0]).strip()
            yield item
