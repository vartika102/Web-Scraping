### -*- coding: utf-8 -*-
##import scrapy
##from scrapy.selector import Selector
##from scrapy.http import Request,FormRequest
##import json
##import re
##import uuid
##import hashlib
##import logging
##import subprocess
##import requests
##import csv
##import io
##import scrapy
##from datetime import datetime
##from collections import OrderedDict
##import os
##from autodata.items import AutodataItem, MetaItem
##from selenium import webdriver
##from selenium.common.exceptions import NoSuchElementException
##
##chromedriver = 'C:/Users/Vartika Singh/Downloads/chromedriver_win32/chromedriver.exe'
##options = webdriver.ChromeOptions()
##options.add_argument('headless')
##args = ["hide_console", ]
##driver = webdriver.Chrome(executable_path=chromedriver, service_args=args, chrome_options=options)
##
##
##class AayanautoSpider(scrapy.Spider):
##    name = 'aayanauto'
##    allowed_domains = []
##    start_urls = []
##    driver.get('http://www.aayanauto.com/en/products/used-cars')
##    driver.implicitly_wait(10)
##    
##    button = driver.find_element_by_xpath('//*[@id="mySearchBut"]')
##    button.click()
##    driver.implicitly_wait(20)
##    pages = driver.find_elements_by_xpath('//*[@id="searchRes"]/div/div[3]/div[2]/ul/li[@class="innerPagingLi"]')
##    page = len(pages)
##    print('#############',page)
##    for page in range(len(pages)):
##        path = driver.find_elements_by_xpath('//*[@id="search_res_used"]/ul/li[@class="  "]/a[1]')
##        for p in path:
##            start_urls.append(p.get_attribute('href'))
##            print(p.get_attribute('href'))
##        nex = driver.find_element_by_link_text('Next').click()
##        driver.implicitly_wait(20)
##        print(nex)
##        #nex.click()
##       #url = path.get_attribute('href')
##    #print(button)
##    
##    
##        
##    #start_urls = ['http://www.aayanauto.com/en/products/used-cars']
##
##    def parse(self, response):
##        paths = response.xpath("//*[@id='latest_cars']/div/ul/li/a")
##        #print(paths)
##        #print(len(paths))
##        for url in paths:
##            url_details = url.xpath("@href").extract()
##            #print(url_details) 
##            url_det = ('http://www.aayanauto.com'+ ''.join(url_details)).strip()
##            #print(url_det)
##            #yield Request (url_det,callback = self.parse_data,dont_filter=True)
##
##
##    def parse_data(self, response):
##        print('done')
##        paths = Selector(response)
##        item2 = MetaItem()
##        item1 = AutodataItem()
##        #details1 = paths.xpath('.//div[@class = car_details')
##        #item1["Car_Name"] = ''.join(paths.xpath('.//table/tbody/tr/td/div/h1[@class = "titled"]//text()').extract()).strip()
##        item1["Last_Code_Update_Date"] = ""
##        item1["Scrapping_Date"] = ""
##        item1["Country"] = "kuwait"
##        item1["City"] = ""
##        item1["Seller_Type"] = "Market Places"
##        item1["Seller_Name"] = "aayanauto"
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
##        item1['mileage_unit'] = 'km'
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
##        sel = response.xpath('//div[@class="car_details"]/ul/li')
##        for s in sel:
##            key = ''.join(s.xpath('div[@class="dt"]/text()').extract()).strip()
##            value = ''.join(s.xpath('div[@class="dd"]/text()').extract()).strip()
##            if key == "Category":
##                item1['Make'] = value
##            elif key == "Model":
##                item1["model"] = value
##            
##            elif key == "Made year":
##                item1["Year"] = value
##            
##            elif key == "KMS":
##                item1["mileage"] = value
##            
##            elif key == "Price":
##                item1["Price_Currency"] = 'KWD'
##                item1['asking_price_inc_VAT'] = value
##
##        item1["Car_Name"] = item1["Make"] + ' ' + item1["model"] + ' ' + item1["Year"]
##
##
##
##
##
##
##
##
##
##
##
##        item2['src'] = "aayanauto.com"
##        item2['ts'] = datetime.utcnow().isoformat()
##        item2['name'] = "aayanauto"
##        item2['url'] = response.url
##        item2['uid'] = str(uuid.uuid4())
##        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
##        item1['meta'] = dict(item2)
##        item1['Last_Code_Update_Date'] = 'Tuesday, June 22, 2019'
##        item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
##        item1['Source'] = item2['src']
##
##        #yield item1
##        
##
##

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
from scrapy_splash import SplashRequest
from autodata.items import AutodataItem, MetaItem

class AayanautohhSpider(scrapy.Spider):
    name = 'aayanauto'
    allowed_domains = []
    start_urls = ['http://www.aayanauto.com/en/products/used-cars']
    urls = ['http://www.aayanauto.com/en/products/used-cars']

    def start_requests(self):
        for url in self.urls:
            yield Request(url,callback=self.parse)


    def parse(self, response):
        #urls = response.xpath('//div[@class="col-sm-3"]/a/@href').extract()
        #print(urls)
        url = "http://www.aayanauto.com/ajaxCalls.php"
        #total = int(response.xpath('//h5[@id="main_pagi"]/b[2]/text()').extract()[0])
        print("ji")
        frmdata = {"showRoooom" : "", "modelID" : '', "carCat": '', "carYearval" : '', "page" : '0', "ajaxType" : "SearchActual", "lang" : 'en', "ajaxCallType" : 'web'}
        yield FormRequest(url, callback = self.parse_len, formdata = frmdata, dont_filter = True)

    def parse_len(self, response):
        data =  json.loads(response.body)
        #total = len(data["pages"])
        url = "http://www.aayanauto.com/ajaxCalls.php"
        #print(response.body)
        for i in range(1,len(data["pages"])+1):
            frmdata = {"showRoooom" : "", "modelID" : '', "carCat": '', "carYearval" : '', "page" : str(i), "ajaxType" : "SearchActual", "lang" : 'en', "ajaxCallType" : 'web'}
            yield FormRequest(url, callback = self.parse_url, formdata = frmdata, dont_filter = True)

    def parse_url(self, response):
        data =  json.loads(response.body)
        for car in data["cars"]:
            item2 = MetaItem()
            item1 = AutodataItem()
            #details1 = paths.xpath('.//div[@class = car_details')
            #item1["Car_Name"] = ''.join(paths.xpath('.//table/tbody/tr/td/div/h1[@class = "titled"]//text()').extract()).strip()
            item1["Last_Code_Update_Date"] = ""
            item1["Scrapping_Date"] = ""
            item1["Country"] = "kuwait"
            item1["City"] = ""
            item1["Seller_Type"] = "Market Places"
            item1["Seller_Name"] = "aayanauto"
            item1["Car_URL"] = response.url
            item1["Car_Name"] = ""
            item1["Year"] = car['madeyear']
            item1["Make"] = car["made"]
            item1["model"] = car['model']
            item1["Car_Name"] = car["made"] + ' ' + car['model'] + ' ' + car['madeyear']
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
            item1["mileage"] = car['addad']
            item1["condition"] = ""
            item1["warranty_untill_when"] = ""
            item1['service_contract_untill_when'] = ''
            item1['Price_Currency'] = 'KWD'
            item1['asking_price_inc_VAT'] = car['price']
            item1['asking_price_ex_VAT'] = ''
            item1['warranty'] = ''
            item1['service_contract'] = ''
            item1['vat'] = 'yes'
            item1['mileage_unit'] = 'km'
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

            item2['src'] = "aayanauto.com"
            item2['ts'] = datetime.utcnow().isoformat()
            item2['name'] = "aayanauto"
            item2['url'] = response.url
            item2['uid'] = str(uuid.uuid4())
            item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
            item1['meta'] = dict(item2)
            item1['Last_Code_Update_Date'] = 'Tuesday, June 22, 2019'
            item1['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
            item1['Source'] = item2['src']

            yield item1
