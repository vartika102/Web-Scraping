"""
        function main(splash)

            splash:runjs("window.location = document.getElementsById('btn_next')[0].href")
            local href = splash:evaljs("document.getElementsById('btn_next')[0].href")
            assert(splash:wait(10))
            local button = splash:select('btn_next')
            button:mouse_click()

            return {
                html = splash:html(),
                png = splash:png(),
                href = href
            }
          end
        """
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

class ArabiaSpider(scrapy.Spider):
    name = 'arabia'
    allowed_domains = []
    start_urls = ['https://www.arabiamotors.com/En/CarLisiting.aspx']
    urls = ['https://www.arabiamotors.com/En/CarLisiting.aspx']

    def start_requests(self):
        for url in self.urls:
            yield SplashRequest(url,callback=self.parse,dont_filter = True)


    def parse(self, response):
        total = int(''.join(response.xpath('//div[@class="site-results-count"]/text()').extract()).strip().split(' ')[0])
        #print("########",total)
        url = "http://www.arabiamotors.com/ASMX_WebServices/asmx_portal.asmx/WS_GetMotorList"
        for page in range(int(total/50)+1):
            #print(page*50)
            frmdata = { 'userid':'0','MotorID':'-1','CategoryID':'-1','MakeID':'-1','ModelID':'-1','FullTypeID':'-1','EngineID':'-1','TransmissionID':'-1','NoOfDoorsID':'-1','DriverTrainID':'-1','OrgineCountryID':'-1','FromYear':'0','ToYear':'0','FromPrice':'0','ToPrice':'0','MillageFrom':'0','MillageTo':'0','licenPlate':'','ExtriorColorID':'-1','IntriorColorID':'-1','KeyWord':'','AdsOnID':'-1','Target':'','LastRow':str(page*50),'WebService_UserName':'web','WebService_UserPassword':'123'}
            yield FormRequest(url, callback=self.parse_data, formdata = frmdata)

    def parse_data(Self, response):
        print("Doing")
        sel = str(response.body)
##        data = json.loads(response.body)
##        motorlist = data['d']['MotorList']
##        sel= ''.join(response.xpath('//input[1]/@value').extract()).strip()
        index = len(sel)-1-sel[::-1].index("}")
        sel = sel[sel.index('{'):index+1]
##        mystring = re.sub("[\\\]", "", dt)
##        mystring = re.sub("\'", "\"", mystring)
##        regex = re.compile(r'[\r\n]')
##        s = regex.sub(" ", dt)
        sel = sel.replace("\\r\\n","")
        sel = sel.replace("\\t","")
        sel = sel.replace('\\','\\\\')
        #sel = sel.replace(&lt;,'')
##        index = sel.index('&lt;')
##        lindex = len(sel)-1-sel[::-1].index(";tg&vid/;tl&")
##        print(index, lindex)
        data = json.loads(sel)
        print(data)
        motorlist = data['d']['MotorList']
        #motorlist = []
        for ml in motorlist:

            item=AutodataItem()
            item2 = MetaItem()
            item["Last_Code_Update_Date"] = ""
            item["Scrapping_Date"] = ""
            item["Country"] = 'Kuwait'
            item["City"] = ""
            item["Seller_Type"] = "Official Dealers"
            item["Seller_Name"] = "Arabia Motors"
            item["Car_URL"] = ""
            item["Car_Name"] = ml['titleen']
            item["Year"] = ml['yearname']
            item["Make"] = ml['brandnameen']
            item["model"] = ml['modelnameen']
            item["Spec"] = ""
            item["Doors"] = ml['noofdoorsnameen']
            item["transmission"] = ml['transmissionnameen']
            item["trim"] = ""
            if ml['categorynameen'] == "Cars and SUVs":
                item["bodystyle"] = 'SUV'
            else:
                item["bodystyle"] = ml['categorynameen']
            item["other_specs_gearbox"] = ""
            item["other_specs_seats"] = ""
            item["other_specs_engine_size"] = ""
            item["other_specs_horse_power"] = ""
            item["colour_exterior"] = ml['exterior_color_en']
            item["colour_interior"] = ml['interior_color_en']
            item["fuel_type"] = ml['fulltypeen']
            item["import_yes_no_also_referred_to_as_GCC_spec"] = "" 
            item["mileage"] = ml['kilometerreading']
            item["condition"] = ml['condition']
            item["warranty_untill_when"] = ""
            item['service_contract_untill_when'] = ''
            item['Price_Currency'] = ml['price'].split(' ')[1]
            item['asking_price_inc_VAT'] = ml['price2']
            item['asking_price_ex_VAT'] = ''
            if ml['warranty'] == 'False':
                item['warranty'] = 'no'
            else:
                item['warranty'] = 'yes'
            item['service_contract'] = ''
            item['vat'] = ''
            item['mileage_unit'] = 'km'
            item['engine_unit'] = 'l'
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
            item['wheel_size'] = ''
            item['top_speed_kph'] = ''
            item['cylinders'] = ml['enginenameen'].split(' ')[0]
            item['acceleration'] = ''
            item['torque_Nm'] = ''

            item2['src'] = "arabiamotors.com"
            item2['ts'] = datetime.utcnow().isoformat()
            item2['name'] = "arabia"
            item2['url'] = response.url
            item2['uid'] = str(uuid.uuid4())
            item2['cs'] = hashlib.md5(json.dumps(dict(item), sort_keys=True).encode('utf-8')).hexdigest()
            item['meta'] = dict(item2)
            item['Car_URL'] = response.url
            item['Source'] = item2['src']
            #yield item

            
##        url = response.xpath('//div[@class="site-results-item-img"]/a/@href').extract()
##        xp = response.xpath('//*[@id="btn_next"]')
##        #element = splash:select('.element')
##        script = """
##        function main(splash)
##
##            local button = splash:select(a.btn_next)
##            button:mouse_click()
##            assert(splash:wait(10))
##
##            return {
##                html = splash:html(),
##                png = splash:png(),
##                href = href
##            }
##          end
##        """
##        #ok = xp[0].click()
##        print(url)
##        #url = 'https://www.arabiamotors.com/En/CarLisiting.aspx'
##        yield SplashRequest(response.url,callback=self.parse_next,dont_filter = True, endpoint='execute',args={'lua_source': script,'wait':'5'})

    def parse_next(self, response):
        print(response.url,'@@@@@@@@@@@',response)

        
##        sel = response.xpath('//div[@class="site-results-item-img"]')
##        print(sel)
##        index = len(sel)-1-sel[::-1].index("}")
##        dt = sel[sel.index('{'):index+1]
##        data = json.loads(dt)
##        print("##########",data)
