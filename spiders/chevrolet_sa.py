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

class SpiderSpider(scrapy.Spider):
    name = 'chevrolet_sa'
    allowed_domains = []
    start_urls = ['https://chevrolet.uma.com.sa/stock/?order=marque,model&page=1&per_page=12']

    def parse(self, response):
        sel = Selector(response)
        yield Request(response.url,callback= self.parse_url,)
        nextt = sel.xpath('//div[@class="pagination"]/div/ul/li[@class="btn-next"]')
        urll = "https://chevrolet.uma.com.sa/stock/" + ''.join(nextt.xpath('a[@title="next page"]/@href').extract()).strip()
        if(nextt != []):
            #print("yess")
            urll = "https://chevrolet.uma.com.sa/stock/" + ''.join(nextt.xpath('a[@title="Next Page"]/@href').extract()).strip()
            yield Request(urll,callback=self.parse,dont_filter = True)
        else:
            print("no")

    def parse_url(self, response):
        sel = Selector(response)
        urls = sel.xpath('//*[@id="content-wrap"]/div[4]/div/div/div[1]/div/div')
        for url in urls:
            new_url = "https://chevrolet.uma.com.sa" + ''.join(url.xpath('.//a[@title="Vehicle Details"]/@href').extract())
            
            yield Request(new_url,callback=self.parse_data,)     
        pass

    def parse_data(self,response):

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
        item1['wheel_size'] = ''
        item1['top_speed_kph'] = ''
        item1['cylinders'] = ''
        item1['acceleration'] = ''
        item1['torque_Nm'] = ''

        sel = Selector(response)
        details1 = sel.xpath('//div[@class = "title module align-center"]')
        details2 = sel.xpath('//div[@class="overview-data module overview-data-standard"]/div/div')
        details3 = sel.xpath('//div[@class="address"]')
        details4 = sel.xpath('//div[@class="price module u-hidden-sm-only"]/div[@class="price-now"]')
        
        item1['Car_URL'] = response.url
        item1['Year'] = ''.join(details1.xpath('h3/span[@class= "year"]//text()').extract()).strip()
        item1['Make'] = ''.join(details1.xpath('h3/span[@class= "make"]//text()').extract()).strip()
        item1['model'] = ''.join(details1.xpath('h3/span[@class= "model"]//text()').extract()).strip()
        item1['Spec'] = ''.join(details1.xpath('h3/span[@class= "variant"]//text()').extract()).strip()
        item1['Car_Name'] = item1['Make'] + ' ' + item1['model'] + ' ' + item1['Spec']

        item1['mileage'] = (''.join(details2.xpath('.//div[@class="cell mileage"]/span[@class="value mileage"]//text()').extract()).strip()).split(' ')[0]
        item1['mileage_unit'] = (''.join(details2.xpath('.//div[@class="cell mileage"]/span[@class="value mileage"]//text()').extract()).strip()).split(' ')[1]
        item1['fuel_type'] = ''.join(details2.xpath('.//div[@class="cell fuel-type"]/span[@class="value fuel-type"]//text()').extract()).strip()
        item1['Doors'] = ''.join(details2.xpath('.//div[@class="cell doors"]/span[@class="value doors"]//text()').extract()).strip()
        item1['other_specs_engine_size'] = (''.join(details2.xpath('.//div[@class="cell engine-size"]/span[@class="value engine-size"]//text()').extract()).strip()).split(' ')[0]
        item1['engine_unit'] = (''.join(details2.xpath('.//div[@class="cell engine-size"]/span[@class="value engine-size"]//text()').extract()).strip()).split(' ')[1]
        item1['trim'] = ''.join(details2.xpath('.//div[@class="cell interior-colour"]/span[@class="value interior-colour"]//text()').extract()).strip()
        item1['transmission'] = ''.join(details2.xpath('.//div[@class="cell transmission"]/span[@class="value transmission"]//text()').extract()).strip()
        item1['bodystyle'] = ''.join(details2.xpath('.//div[@class="cell bodystyle"]/span[@class="value bodystyle"]//text()').extract()).strip()
        item1['colour_exterior'] = ''.join(details2.xpath('.//div[@class="cell exterior-colour"]/span[@class="value exterior-colour"]//text()').extract()).strip()

        item1['City'] = ''.join(details3.xpath('span[@class="address-city"]//text()').extract()).strip()
        item1['Country'] = 'Saudi Arabia'
        item1['Price_Currency'] = (''.join(details4.xpath('span[@class="value"]//text()').extract()).strip())[:3]
        item1['asking_price_inc_VAT'] = (''.join(details4.xpath('span[@class="value"]//text()').extract()).strip())[3:]

        item2['src'] = "chevrolet.uma.com.sa"
        item2['ts'] = datetime.utcnow().isoformat()
        item2['name'] = "spider"
        item2['url'] = response.url
        item2['uid'] = str(uuid.uuid4())
        item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
        item1['meta'] = dict(item2)
        item1['Last_Code_Update_Date'] = 'June 6, 2019'
        item1['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')
        item1['Seller_Name'] = 'Universal Motors Agencies'
        item1['Source'] = item2['src']
        yield item1
        
