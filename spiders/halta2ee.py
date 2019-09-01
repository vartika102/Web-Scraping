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

class Halta2eeSpider(scrapy.Spider):
    name = 'halta2ee'
    allowed_domains = []
    start_urls = ['https://uae.hatla2ee.com/en/car']

    def parse(self,response):
        sel = Selector(response)
        yield Request(response.url, callback = self.parse_url, dont_filter = True)
        #path = sel.xapth('div[@class="pagination pagination-right"
        length = (sel.xpath('//a[@class="paginate"]')[-1])
        data = ''.join(length.xpath('text()').extract()).strip()
        #print("####",data,"@@@@@", 'Next >>')
        if data == 'Next »':
            yield Request('https://uae.hatla2ee.com' + ''.join(length.xpath('@href').extract()).strip(),callback = self.parse, dont_filter = True)
            #print("#######",data)
        pass
##        for l in length:
##            url = 'https://uae.hatla2ee.com/en/car/page/' + str(l+1)
##            yield Request(url, callback = self.parse_url, dont_filter = True)

    def parse_url(self, response):
        sel = Selector(response)
        divs = sel.xpath('//div[@class="CarListWrapper"]/div[@class="CarListUnit row-fluid "]')
        print("########",len(divs))
        for div in divs:
            url = 'https://uae.hatla2ee.com' + ''.join(div.xpath('.//a[@class="NewListTitle"]/@href').extract()).strip()
            yield Request(url, callback = self.parse_data, dont_filter = True)
        pass

    def parse_data(self, response):
        #print("YAY!")
        item2 = MetaItem()
        item1 = AutodataItem()
        sel = Selector(response)

        item1["Last_Code_Update_Date"] = ""
        item1["Scrapping_Date"] = ""
        item1["Country"] = "UAE"
        item1["City"] = ""
        item1["Seller_Type"] = ""
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

        details = sel.xpath('//div[@class="hSectionContent nUnitKeyDetailsContent clearfix"]/div[@class="nUnitKeyDetails"]')
        print(len(details))
        for det in details:
            key = ''.join(det.xpath('span/text()').extract()).strip()
            value = ''.join(det.xpath('strong/text()').extract()).strip()
            if key == 'Model':
                item1["model"] = value
            elif key == 'Make':
                item1["Make"] = value
            elif key == 'City':
                item1["City"] = value
            elif key == 'Color':
                item1["colour_exterior"] = value
            elif key == 'Transmission':
                item1["transmission"] = value
            elif key == 'Body style':
                item1["bodystyle"] = value
            elif key == 'Price':
                item1["Price_Currency"] = value.split(' ')[1]
                item1['asking_price_inc_VAT'] = value.split(' ')[0]
                item1['vat'] = 'yes'
            elif key == 'Fuel':
                item1["fuel_type"] = value
            elif key == 'Used since':
                item1["Year"] = value
            elif key == 'Km':
                item1['mileage'] = value.split(' ')[0]
                item1['mileage_unit'] = 'km'

        item1["Car_Name"] = ''.join(sel.xpath('//div[@class="nUnitShow"]//h1/text()').extract()).strip().replace('Used ','')
        item2['src'] = "uae.hatla2ee.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "hatla2ee"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Source'] = item2['src']
        item1['Last_Code_Update_Date'] = 'Tuesday, June 18, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')

        if item1['Car_Name'] != '':
            yield item1
##        else:
##            yield Request(response.url, callback = self.parse_url2, dont_filter = True)
        pass

##    def parse_url2(self, response):
##        sel = Selector(response)
##        divs = sel.xpath('//div[@class="CarListWrapper"]/div[@class="CarListUnit row-fluid "]')
##        print("########",len(divs))
##        for div in divs:
##            url = 'https://uae.hatla2ee.com' + ''.join(div.xpath('.//a[@class="NewListTitle"]/@href').extract()).strip()
##            yield Request(url, callback = self.parse_data2, dont_filter = True)
##        pass
##
##    def parse_data2(self, response):
##        #print("YAY!")
##        item2 = MetaItem()
##        item1 = AutodataItem()
##        sel = Selector(response)
##
##        item1["Last_Code_Update_Date"] = ""
##        item1["Scrapping_Date"] = ""
##        item1["Country"] = "UAE"
##        item1["City"] = ""
##        item1["Seller_Type"] = ""
##        item1["Seller_Name"] = ""
##        item1["Car_URL"] = response.url
##        item1["Car_Name"] = ""
##        item1["Year"] = ""
##        item1["Make"] = ""
##        item1["model"] = ""
##        item1["Spec"] = ""
##        item1["Doors"] = ""
##        item1["transmission"] = ""
##        item1["trim"] = ""
##        item1["bodystyle"] = ""
##        item1["other_specs_gearbox"] = ""
##        item1["other_specs_seats"] = ""
##        item1["other_specs_engine_size"] = ""
##        item1["other_specs_horse_power"] = ""
##        item1["colour_exterior"] = ""
##        item1["colour_interior"] = ""
##        item1["fuel_type"] = ""
##        item1["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
##        item1["mileage"] = ""
##        item1["condition"] = ""
##        item1["warranty_untill_when"] = ""
##        item1['service_contract_untill_when'] = ''
##        item1['Price_Currency'] = ''
##        item1['asking_price_inc_VAT'] = ''
##        item1['asking_price_ex_VAT'] = ''
##        item1['warranty'] = ''
##        item1['service_contract'] = ''
##        item1['vat'] = 'yes'
##        item1['mileage_unit'] = ''
##        item1['engine_unit'] = ''
##        item1['autodata_Make'] = ''
##        item1['autodata_Make_id'] = ''
##        item1['autodata_model'] = ''
##        item1['autodata_model_id'] = ''
##        item1['autodata_Spec'] = ''
##        item1['autodata_Spec_id'] = ''
##        item1['autodata_transmission'] = ''
##        item1['autodata_transmission_id'] = ''
##        item1['autodata_bodystyle'] = ''
##        item1['autodata_bodystyle_id'] = ''
##
##        details = sel.xpath('//div[@class="hSectionContent nUnitKeyDetailsContent clearfix"]/div[@class="nUnitKeyDetails"]')
##        print(len(details))
##        for det in details:
##            key = ''.join(det.xpath('span/text()').extract()).strip()
##            value = ''.join(det.xpath('strong/text()').extract()).strip()
##            if key == 'Model':
##                item1["model"] = value
##            elif key == 'Make':
##                item1["Make"] = value
##            elif key == 'City':
##                item1["City"] = value
##            elif key == 'Color':
##                item1["colour_exterior"] = value
##            elif key == 'Transmission':
##                item1["transmission"] = value
##            elif key == 'Body style':
##                item1["bodystyle"] = value
##            elif key == 'Price':
##                item1["Price_Currency"] = value.split(' ')[1]
##                item1['asking_price_inc_VAT'] = value.split(' ')[0]
##                item1['vat'] = 'yes'
##            elif key == 'Fuel':
##                item1["fuel_type"] = value
##            elif key == 'Used since':
##                item1["Year"] = value
##            elif key == 'Km':
##                item1['mileage'] = value.split(' ')[0]
##                item1['mileage_unit'] = 'km'
##
##        item1["Car_Name"] = ''.join(sel.xpath('//div[@class="nUnitShow"]//h1/text()').extract()).strip().replace('Used ','')
##        item2['src'] = "uae.hatla2ee.com"
##        item2['ts'] = datetime.utcnow().isoformat()
##        item2['name'] = "hatla2ee"
##        item2['url'] = response.url
##        item2['uid'] = str(uuid.uuid4())
##        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
##        item1['meta'] = dict(item2)
##        item1['Source'] = item2['src']
##        item1['Last_Code_Update_Date'] = 'Tuesday, June 18, 2019'
##        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
##
##        if item1['Car_Name'] != '':
##            yield item1
##        else:
##            yield Request(response.url, callback = self.parse_url3, dont_filter = True)
##        pass
##
##    def parse_url3(self, response):
##        sel = Selector(response)
##        divs = sel.xpath('//div[@class="CarListWrapper"]/div[@class="CarListUnit row-fluid "]')
##        print("########",len(divs))
##        for div in divs:
##            url = 'https://uae.hatla2ee.com' + ''.join(div.xpath('.//a[@class="NewListTitle"]/@href').extract()).strip()
##            yield Request(url, callback = self.parse_data3, dont_filter = True)
##        pass
##
##    def parse_data3(self, response):
##        #print("YAY!")
##        item2 = MetaItem()
##        item1 = AutodataItem()
##        sel = Selector(response)
##
##        item1["Last_Code_Update_Date"] = ""
##        item1["Scrapping_Date"] = ""
##        item1["Country"] = "UAE"
##        item1["City"] = ""
##        item1["Seller_Type"] = ""
##        item1["Seller_Name"] = ""
##        item1["Car_URL"] = response.url
##        item1["Car_Name"] = ""
##        item1["Year"] = ""
##        item1["Make"] = ""
##        item1["model"] = ""
##        item1["Spec"] = ""
##        item1["Doors"] = ""
##        item1["transmission"] = ""
##        item1["trim"] = ""
##        item1["bodystyle"] = ""
##        item1["other_specs_gearbox"] = ""
##        item1["other_specs_seats"] = ""
##        item1["other_specs_engine_size"] = ""
##        item1["other_specs_horse_power"] = ""
##        item1["colour_exterior"] = ""
##        item1["colour_interior"] = ""
##        item1["fuel_type"] = ""
##        item1["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
##        item1["mileage"] = ""
##        item1["condition"] = ""
##        item1["warranty_untill_when"] = ""
##        item1['service_contract_untill_when'] = ''
##        item1['Price_Currency'] = ''
##        item1['asking_price_inc_VAT'] = ''
##        item1['asking_price_ex_VAT'] = ''
##        item1['warranty'] = ''
##        item1['service_contract'] = ''
##        item1['vat'] = 'yes'
##        item1['mileage_unit'] = ''
##        item1['engine_unit'] = ''
##        item1['autodata_Make'] = ''
##        item1['autodata_Make_id'] = ''
##        item1['autodata_model'] = ''
##        item1['autodata_model_id'] = ''
##        item1['autodata_Spec'] = ''
##        item1['autodata_Spec_id'] = ''
##        item1['autodata_transmission'] = ''
##        item1['autodata_transmission_id'] = ''
##        item1['autodata_bodystyle'] = ''
##        item1['autodata_bodystyle_id'] = ''
##
##        details = sel.xpath('//div[@class="hSectionContent nUnitKeyDetailsContent clearfix"]/div[@class="nUnitKeyDetails"]')
##        print(len(details))
##        for det in details:
##            key = ''.join(det.xpath('span/text()').extract()).strip()
##            value = ''.join(det.xpath('strong/text()').extract()).strip()
##            if key == 'Model':
##                item1["model"] = value
##            elif key == 'Make':
##                item1["Make"] = value
##            elif key == 'City':
##                item1["City"] = value
##            elif key == 'Color':
##                item1["colour_exterior"] = value
##            elif key == 'Transmission':
##                item1["transmission"] = value
##            elif key == 'Body style':
##                item1["bodystyle"] = value
##            elif key == 'Price':
##                item1["Price_Currency"] = value.split(' ')[1]
##                item1['asking_price_inc_VAT'] = value.split(' ')[0]
##                item1['vat'] = 'yes'
##            elif key == 'Fuel':
##                item1["fuel_type"] = value
##            elif key == 'Used since':
##                item1["Year"] = value
##            elif key == 'Km':
##                item1['mileage'] = value.split(' ')[0]
##                item1['mileage_unit'] = 'km'
##
##        item1["Car_Name"] = ''.join(sel.xpath('//div[@class="nUnitShow"]//h1/text()').extract()).strip().replace('Used ','')
##        item2['src'] = "uae.hatla2ee.com"
##        item2['ts'] = datetime.utcnow().isoformat()
##        item2['name'] = "hatla2ee"
##        item2['url'] = response.url
##        item2['uid'] = str(uuid.uuid4())
##        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
##        item1['meta'] = dict(item2)
##        item1['Source'] = item2['src']
##        item1['Last_Code_Update_Date'] = 'Tuesday, June 18, 2019'
##        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
##
##        if item1['Car_Name'] != '':
##            yield item1
##        else:
##            yield Request(response.url, callback = self.parse_url4, dont_filter = True)
##        pass
##
##
##
##    def parse_url4(self, response):
##        sel = Selector(response)
##        divs = sel.xpath('//div[@class="CarListWrapper"]/div[@class="CarListUnit row-fluid "]')
##        print("########",len(divs))
##        for div in divs:
##            url = 'https://uae.hatla2ee.com' + ''.join(div.xpath('.//a[@class="NewListTitle"]/@href').extract()).strip()
##            yield Request(url, callback = self.parse_data4, dont_filter = True)
##        pass
##
##    def parse_data4(self, response):
##        #print("YAY!")
##        item2 = MetaItem()
##        item1 = AutodataItem()
##        sel = Selector(response)
##
##        item1["Last_Code_Update_Date"] = ""
##        item1["Scrapping_Date"] = ""
##        item1["Country"] = "UAE"
##        item1["City"] = ""
##        item1["Seller_Type"] = ""
##        item1["Seller_Name"] = ""
##        item1["Car_URL"] = response.url
##        item1["Car_Name"] = ""
##        item1["Year"] = ""
##        item1["Make"] = ""
##        item1["model"] = ""
##        item1["Spec"] = ""
##        item1["Doors"] = ""
##        item1["transmission"] = ""
##        item1["trim"] = ""
##        item1["bodystyle"] = ""
##        item1["other_specs_gearbox"] = ""
##        item1["other_specs_seats"] = ""
##        item1["other_specs_engine_size"] = ""
##        item1["other_specs_horse_power"] = ""
##        item1["colour_exterior"] = ""
##        item1["colour_interior"] = ""
##        item1["fuel_type"] = ""
##        item1["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
##        item1["mileage"] = ""
##        item1["condition"] = ""
##        item1["warranty_untill_when"] = ""
##        item1['service_contract_untill_when'] = ''
##        item1['Price_Currency'] = ''
##        item1['asking_price_inc_VAT'] = ''
##        item1['asking_price_ex_VAT'] = ''
##        item1['warranty'] = ''
##        item1['service_contract'] = ''
##        item1['vat'] = 'yes'
##        item1['mileage_unit'] = ''
##        item1['engine_unit'] = ''
##        item1['autodata_Make'] = ''
##        item1['autodata_Make_id'] = ''
##        item1['autodata_model'] = ''
##        item1['autodata_model_id'] = ''
##        item1['autodata_Spec'] = ''
##        item1['autodata_Spec_id'] = ''
##        item1['autodata_transmission'] = ''
##        item1['autodata_transmission_id'] = ''
##        item1['autodata_bodystyle'] = ''
##        item1['autodata_bodystyle_id'] = ''
##
##        details = sel.xpath('//div[@class="hSectionContent nUnitKeyDetailsContent clearfix"]/div[@class="nUnitKeyDetails"]')
##        print(len(details))
##        for det in details:
##            key = ''.join(det.xpath('span/text()').extract()).strip()
##            value = ''.join(det.xpath('strong/text()').extract()).strip()
##            if key == 'Model':
##                item1["model"] = value
##            elif key == 'Make':
##                item1["Make"] = value
##            elif key == 'City':
##                item1["City"] = value
##            elif key == 'Color':
##                item1["colour_exterior"] = value
##            elif key == 'Transmission':
##                item1["transmission"] = value
##            elif key == 'Body style':
##                item1["bodystyle"] = value
##            elif key == 'Price':
##                item1["Price_Currency"] = value.split(' ')[1]
##                item1['asking_price_inc_VAT'] = value.split(' ')[0]
##                item1['vat'] = 'yes'
##            elif key == 'Fuel':
##                item1["fuel_type"] = value
##            elif key == 'Used since':
##                item1["Year"] = value
##            elif key == 'Km':
##                item1['mileage'] = value.split(' ')[0]
##                item1['mileage_unit'] = 'km'
##
##        item1["Car_Name"] = ''.join(sel.xpath('//div[@class="nUnitShow"]//h1/text()').extract()).strip().replace('Used ','')
##        item2['src'] = "uae.hatla2ee.com"
##        item2['ts'] = datetime.utcnow().isoformat()
##        item2['name'] = "hatla2ee"
##        item2['url'] = response.url
##        item2['uid'] = str(uuid.uuid4())
##        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
##        item1['meta'] = dict(item2)
##        item1['Source'] = item2['src']
##        item1['Last_Code_Update_Date'] = 'Tuesday, June 18, 2019'
##        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
##
##        if item1['Car_Name'] != '':
##            yield item1
##        
##        pass
##    
