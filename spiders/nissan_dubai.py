# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
from scrapy.linkextractors import LinkExtractor
import requests
import json
import re
import uuid
import hashlib
import logging
import subprocess
import json
from datetime import datetime,date
from autodata.items import AutodataItem, MetaItem

class NissanSpider(scrapy.Spider):
    name = 'nissan_dubai'
    allowed_domains = []
    start_urls = ['http://www.aac-usedcars.com/nissan/load.php?mark=NISSAN']

    def parse(self, response):
        sel = Selector(response)
        data =  json.loads(response.body)
        body = "".join(map(chr, response.body))
        i = 0
        count = 0
        while (count<len(data)):
            d = str(i)
            if d in data:
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
                item1['vat'] = ''
                item1["mileage_unit"] = 'km'
                item1["engine_unit"] = ''
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

                print("Yes")
                item1["Seller_Type"] = data[d]["SALE_TYPE"]
                item1["Seller_Name"] = data[d]["SELLER_NAME"]
                item1["Car_Name"] = data[d]["DESCRIPTION"]
                item1["Year"] = str(data[d]["MODEL_YEAR"])
                item1["Make"] = data[d]["MAKE_DESC"]
                item1["model"] = data[d]["MODEL_DESC"]
                item1["bodystyle"] = data[d]["BODY_TYPE_DESC"]
                item1["other_specs_engine_size"] = data[d]["ENGINE_SIZE"].split(' ')[0]
                item1["engine_unit"] = data[d]["ENGINE_SIZE"].split(' ')[1]
                item1["colour_exterior"] = data[d]["COLOR"]
                item1["fuel_type"] = data[d]["FUEL_TYPE_DESC"]
                item1["mileage"] = data[d]["MILEAGE"]
                item1["Spec"] = data[d]["VARIANT"]
                item1["trim"] = data[d]["TRIM_TYPE"]
                item1["colour_interior"] = data[d]["INTERIOR_COLOR"]
                item1["City"] = "Dubai"
                item1["asking_price_inc_VAT"] = data[d]["PRICE"]
                item1["Price_Currency"] = "AED"
                item1["Country"] = "Saudi Arabia"
                item1["vat"] = "yes"
                item1["Car_URL"] = "https://en.nissan-dubai.com/certified-preowned-cars/buy-a-car.html"
                if data[d]["TRNS_TYPE_DESC"] == "A/T":
                    item1["transmission"] = "Automatic"
                else:
                    item1["transmission"] = data[d]["TRNS_TYPE_DESC"]
                item1["warranty_untill_when"] = data[d]["WAR_EXP_DATE"]
                if item1["warranty_untill_when"] != "":
                    item1["warranty"] = "yes"
                item2['src'] = "en.nissan-dubai.com"
                item2['ts'] = datetime.utcnow().isoformat()
                item2['name'] = "nissan"
                item2['url'] = response.url
                item2['uid'] = str(uuid.uuid4())
                item2['cs'] = hashlib.md5(json.dumps(dict(item1), sort_keys=True).encode('utf-8')).hexdigest()
                item1['meta'] = dict(item2)
                item1['Source'] = item2['src']
                item1['Last_Code_Update_Date'] = 'June 7, 2019'
                item1['Scrapping_Date'] = datetime.today().strftime('%Y-%m-%d')
                count = count+1
                yield item1
            i = i+1
        print(count, i)
        pass
