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

class CarDohaSpider(scrapy.Spider):
    name = 'cardoha'
    allowed_domains = []
    start_urls = ['http://carsindoha.com/car-listing/']
    urls = ['http://carsindoha.com/car-listing/']

    def start_requests(self):
        for url in self.urls:
            yield Request(url,callback=self.parse)


    def parse(self, response):
        #urls = response.xpath('//div[@class="col-sm-3"]/a/@href').extract()
        #print(urls)
        url = "http://carsindoha.com/wp-admin/admin-ajax.php"
        total = int(response.xpath('//h5[@id="main_pagi"]/b[2]/text()').extract()[0])
        print(total)
        for i in range(1,total+1):
            frmdata = {"action" : "get_pagi_post", "page_id" : str(i), "page_post": "car_listening"}
            yield FormRequest(url, callback = self.parse_url, formdata = frmdata, dont_filter = True)

    def parse_url(self, response):
        urls = response.xpath('//div[@class="col-sm-3"]/a/@href').extract()
        print(len(urls))
        for url in urls:
            i =0 
            yield Request(url, callback = self.parse_data, dont_filter = True)

    def parse_data(self, response):
        print("onn")

        dd = response.xpath('//div[@class="sp-product-info"]/h5/text()').extract()
        print(dd)
        item=AutodataItem()
        item2 = MetaItem()
        item["Last_Code_Update_Date"] = ""
        item["Scrapping_Date"] = ""
        item["Country"] = "Qatar"
        item["City"] = ""
        item["bodystyle"] = ""
        item["Seller_Type"] = "Market Places"
        item["Seller_Name"] = "Cars in Doha"
        item["Car_URL"] = response.url
        item["Car_Name"] = "".join(response.xpath('/html/body/section[2]/div/ul/li[4]//text()').extract()).strip()
        words = item['Car_Name'].split()
        item['Car_Name'] = " ".join(sorted(set(words), key=words.index))
        res = [i for i in words if '.' in i]
        item["Year"] = item['Car_Name'].split(' ')[-1]
        try:
            int(item['Year'])
        
        except ValueError:
            item['Year'] = ''
        item["Make"] = item['Car_Name'].split(' ')[0]
        item["model"] = ""
        item["Spec"] = ""
        item["Doors"] = ""
        item["transmission"] = "".join(dd[2]).strip()
        item["trim"] = ""
        if len(dd) > 4:
            item["bodystyle"] = "".join(dd[4]).split('/')[-1].strip()
        item["other_specs_gearbox"] = ""
        item["other_specs_seats"] = ""
        if res != []:
            item["other_specs_engine_size"] = res[0].replace('L','').replace('T','')
            item['engine_unit'] = 'l'
            item['Car_Name'] = item['Car_Name'].replace(res[0]+' ','')
        else:
            item["other_specs_engine_size"] = ''
            item['engine_unit'] = ''
        item["other_specs_horse_power"] = ""
        item["colour_exterior"] = "".join(dd[0]).strip()
        item["colour_interior"] = ""
        item["fuel_type"] = ""
        item["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
        item["mileage"] = "".join(dd[1]).strip().split(' ')[0]
        item['mileage_unit'] = "KM"
        if item['mileage'] == "KM":
            item['mileage'] = ''
        item["condition"] = ""
        item["warranty_untill_when"] = ""
        item['service_contract_untill_when'] = ''
        item['Price_Currency'] = 'QR'
        item['asking_price_inc_VAT'] = ''.join(response.xpath('//div[@class="col-sm-12 text-center"]/span/text()').extract()).strip().split(' ')[-1]
        if item['asking_price_inc_VAT'] == 'QR':
            item['asking_price_inc_VAT'] = ''
        item['asking_price_ex_VAT'] = ''
        item['warranty'] = ''
        item['service_contract'] = ''
        item['vat'] = 'yes'
                
        item['Last_Code_Update_Date'] = 'Thursday, June 07, 2019'
        item['Scrapping_Date'] = datetime.today().strftime('%A, %B %d, %Y')
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

        item2['src'] = "carsindoha.com"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "cardoha"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
        item['meta'] = dict(item2)
        item['Car_URL'] = response.url
        item['Source'] = item2['src']

        

        dt = ''.join(response.xpath('//div[@class="sp-single-content"]/div[@class="col-sm-12 desc-content"]/text()').extract()).strip()
        print('############',res)

        yield item

