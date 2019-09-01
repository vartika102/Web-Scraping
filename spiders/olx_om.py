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

class OlxOmSpider(scrapy.Spider):
    name = 'olx_om'
    allowed_domains = []
    start_urls = ['https://olx.com.om/en/vehicles/cars/?page=1']

    def parse(self,response):
        #yield Request(response.url, callback = self.parse_url, dont_filter = True)
        sel = Selector(response)
        next_url = ''.join(sel.xpath('//span[@class="item fright"]/a/@href').extract()).strip()
        total = sel.xpath('//span[@class="item fleft"]/a/span/text()').extract()[-1]
        print("#########",int(total))
        for i in range(1,int(total)+1):
            next_url = 'https://olx.com.om/en/vehicles/cars/?page=' + str(i)
            yield Request(next_url, callback = self.parse_url, dont_filter = True)
##        if next_url != '':
##            yield Request(next_url, callback = self.parse, dont_filter = True)

    def parse_url(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="ads ads--list"]//div[@class="ads__item__info"]')
        print(len(urls))
        for url in urls:
            new_url = ''.join(url.xpath('a/@href').extract()).strip().replace('.om','.om/en')
            print("||||||||||||||||||",new_url)
            yield Request(new_url, callback = self.parse_data, dont_filter = True)

    def parse_data(self, response):
        item2 = MetaItem()
        item1 = AutodataItem()
        sel = Selector(response)

        item1["Last_Code_Update_Date"] = ""
        item1["Scrapping_Date"] = ""
        item1["Country"] = "Oman"
        item1["City"] = ""
        item1["Seller_Type"] = "Market Places"
        item1["Seller_Name"] = ""
        item1["Car_URL"] = response.url
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
        
        item2['src'] = "olx.com.om"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "olx_om"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Source'] = item2['src']
        item1['Last_Code_Update_Date'] = 'Tuesday, June 18, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')

        #det = ''.join(sel.xpath('//div[@class="lang-selector small"]/ul/li[@class="inlblk"]/a[@class="x-normal"]/@href').extract()).strip()
        dets = sel.xpath('//table[@class="item"]//tr')
        for det in dets:
            
            key = ''.join(det.xpath('th/text()').extract()).strip()
            value = ''.join(det.xpath('td//text()').extract()).strip()
            #print(key,value)
            if key == 'Model':
                item1["model"] = value
            elif key == 'Transmission Type':
                item1["transmission"] = value
            elif key == 'Year':
                item1["Year"] = value
            elif key == 'Color':
                item1["colour_exterior"] = value
            elif key == 'Body Type':
                item1["bodystyle"] = value
            elif key == 'Kilometers':
                item1["mileage"] = value.split(' ')[0]
            elif key == 'Warranty':
                item1['warranty'] = value
                if value == 'Does Not Apply':
                    item1['warranty'] = ''
        item1['asking_price_inc_VAT'] = ''.join(sel.xpath('//div[@class="pricelabel tcenter"]//text()').extract()).strip().split(' ')[0]
        item1['Price_Currency'] = 'OMR'
        item1["City"] = ''.join(sel.xpath('//strong[@class="c2b small"]//text()').extract()).strip().split(' ')[-1]
        item1['Make'] = ''.join(sel.xpath('//ul[@class="clearfix"]/li[4]//span/text()').extract()).strip().split(' ')[0][1:]
        item1['Car_Name'] = item1['Make'] + ' ' + item1['model']
        
        yield item1
        #print("########",key, value)


