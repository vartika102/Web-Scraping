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
from autodata.items import AutodataItem, MetaItem

class ZmotorsSpider(scrapy.Spider):
    name = "zmotors"
    allowed_domains = []
    urls = []
    start_urls = ["https://www.zmotors.com/preowned/"]
        
    def parse(self, response):
        last_page = response.xpath("//span[contains(@class,'manage_title')]/strong/text()").extract()[0]
        last = int(last_page.split()[-1])
        for i in range(1, last+1):
            pages = str.join('',('https://www.zmotors.com/preowned/page/',str(i),'/'))
            yield(scrapy.Request(pages, callback=self.parse1))

    def parse1(self, response):
        for href in response.xpath("//div[contains(@class,'offer_aside')]/h2/a/@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
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
        item1['vat'] = 'yes'
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
        item1['Last_Code_Update_Date'] = 'June 17, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')

        car_name = response.xpath("//div[contains(@class,'col_1_01')]/h1/text()").extract()[0]
        if car_name!= "Ramadan Deals":
            item1['Last_Code_Update_Date'] = "17 June 2019"
            item1['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')
            item1['Country'] = 'Bahrain'
            item1['City'] = 'Manama'
            item1['Seller_Type'] = 'Large Independent Dealers'
            item1['Seller_Name'] = 'Zayani Motors'
            item1['Car_URL'] = response.url
            item1['Car_Name'] = car_name
            car = car_name.split()[0]
            if car=="MG":
                item1['Make'] = 'MG'
                item1['model']= (car_name.replace("MG",'')).strip()
            if car=="Lexus":
                item1['Make'] = "Lexus"
                item1['model'] = (car_name.replace("Lexus",'')).strip()
            mod = ["Lancer","L200","Attrage","Pajero","Outlander","Montero","Mast"]
            for m in mod:
                if m in item1['Car_Name']:
                        item1['Make'] = "Mitsubishi"
                        item1['model'] = m

            item1['Year'] = response.xpath("//div[contains(@class,'offer_data')]/ul/li/text()").extract()[0]
            item1['asking_price_inc_VAT']= response.xpath("//div[contains(@class,'offer_price')]/strong/text()").extract()[0].split()[0]

            item1['Price_Currency'] = 'BHD'
            item1['colour_exterior']= ''
            mil=(response.xpath("//div[contains(@class,'offer_data')]/ul/li/text()").extract()[1]).split()[0]
            if mil=="KM":
                item1['mileage'] = ''
            else:
                item1['mileage'] = mil
            item1['mileage_unit'] = 'km'
            item1['fuel_type']=response.xpath("//div[contains(@class,'offer_data')]/ul/li/text()").extract()[2]
            item2['src'] = "zmotors.com"
            item2['ts'] = datetime.utcnow().isoformat()
            item2['name'] = "zmotors"
            item2['url'] = response.url
            item2['uid'] = str(uuid.uuid4())
            item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
            item1['meta'] = dict(item2)
            item1['Source'] = item2['src']
            yield item1
