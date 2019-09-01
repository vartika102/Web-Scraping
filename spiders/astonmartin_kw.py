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

class AstonmartinKwscrapySpider(scrapy.Spider):
    name = "astonmartin_kw"
    allowed_domains = []
    urls = []
    start_urls = ["https://preowned.astonmartin.com/preowned-cars/search/?continent-country%5B%5D=Kuwait&finance%5B%5D=price&location%5B%5D=4f7ecda9582216a7badad34d72574ae52af11d67&condition%5B%5D=used&section%5B%5D=5&order=-usd_price&pageId=13"]
        
    def parse(self,response):
        for href in response.xpath("//div[contains(@class, 'title module')]/h3/a//@href"):
            url="https://preowned.astonmartin.com"+href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)
    
    def parse_dir_contents(self,response):
        item=AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = ''.join(response.xpath('//span[@class = "address-country"]/text()').extract()).strip()
        item["City"] = ''.join(response.xpath('//span[@class = "address-city"]/text()').extract()).strip()
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
        item['Last_Code_Update_Date'] = 'June 6, 2019'
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

        item2['src'] = "astonmartin.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "astonmartin_kw"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']
            
        item['asking_price_inc_VAT'] = ''.join(response.xpath("//div[contains(@class,'price-now')]/span[contains(@class,'value')]/text()").extract()).strip().split(' ')[1]
        item['Price_Currency'] = ''.join(response.xpath("//div[contains(@class,'price-now')]/span[contains(@class,'value')]/text()").extract()).strip().split(' ')[0]
        item['Year'] = response.xpath("//div[contains(@class, 'title module align-center')]/h3/span[contains(@class, 'year')]/text()").extract()[0].strip()
        item['Make'] = response.xpath("//div[contains(@class, 'title module align-center')]/h3/span[contains(@class, 'make')]/text()").extract()[0].strip()
        item['model'] = response.xpath("//div[contains(@class, 'title module align-center')]/h3/span[contains(@class, 'model')]/text()").extract()[0].strip()
        item['transmission'] = response.xpath("//div[contains(@class, 'cell transmission')]/span[contains(@class, 'value transmission')]/text()").extract()[0].strip()
        
        item['mileage'] = ((response.xpath("//div[contains(@class, 'cell mileage')]/span[contains(@class, 'value mileage')]/text()").extract()[0]).split('km')[0]).strip()
        item['mileage_unit'] = 'km'
        item['other_specs_engine_size'] = ((response.xpath("//div[contains(@class, 'span6')]/div[contains(@class,'custom-html module align-center tech-spec')]/table/tr/td[contains(@class,'value')]/text()").extract()[0]).split('Litre')[0]).strip()
        item['engine_unit'] = 'Litre'
        item['colour_exterior'] = response.xpath("//div[contains(@class, 'cell exterior-colour')]/span[contains(@class, 'value exterior-colour')]/text()").extract()[0].strip()
        item['other_specs_horse_power'] = ((response.xpath("//div[contains(@class, 'span6')]/div[contains(@class,'custom-html module align-center tech-spec')]/table/tr/td[contains(@class,'value')]/text()").extract()[3]).split("BHP")[0]).strip()
        
        item['colour_interior'] = response.xpath("//div[contains(@class, 'cell interior-colour')]/span[contains(@class, 'value interior-colour')]/text()").extract()[0].strip()
        item['bodystyle'] = (response.xpath("//div[contains(@class, 'title module align-center')]/h3/span[contains(@class, 'variant')]/text()").extract()[0]).split()[-1]
        item['Car_Name'] = item['Make'] + ' ' + item['model'] + ' ' + item['bodystyle']        
        
        yield item





