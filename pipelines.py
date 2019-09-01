# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutodataPipeline(object):
    def process_item(self, item, spider):
        return item

import csv
from pymongo import MongoClient
from fuzzywuzzy import process

class MongoPipeline(object):

    def open_spider(self, spider):
##        uncomment if want to store data in MongoDB
##        from autodata.config import mongoConfiguration
##        mongoConfig = mongoConfiguration.get(spider.name)
##        client = MongoClient(mongoConfig.get('MONGODB_HOST', 'localhost'), mongoConfig.get('MONGODB_PORT', 27017))
##        db = client[mongoConfig.get('MONGODB_DATABASE_NAME')]
##        self.col = db[mongoConfig.get('MONGODB_COLLECTION_NAME')]

        '''self.conn = MongoClient('localhost', 27017)
        db = self.conn["autodata"]
        self.collection = db['']'''
        self.body_type = {}
        self.transmission = {}
        self.make_ = {}
        self.model_ = {}
        self.spec_ = {}
        self.lis = []
        with open('C:/Users/Vartika Singh/autodata/autodata/body_type.csv') as fin:
                  reader = csv.reader(fin)
                  for row in reader:
                      self.body_type.update({row[1]:row[0]})
        with open('C:/Users/Vartika Singh/autodata/autodata/transmission.csv') as fin:
                  reader = csv.reader(fin)
                  for row in reader:
                      self.transmission.update({row[1]:row[0]})
        with open('C:/Users/Vartika Singh/autodata/autodata/make-model-spec.csv') as fin:
                  reader = csv.reader(fin)
                  for row in reader:
                      self.make_.update({row[1]:row[0]})
                      self.lis.append(row)
        
    def process_item(self, item, spider):
        if 'saloon' in item["bodystyle"].lower():
            item['bodystyle'] = 'Sedan'
        body = item["bodystyle"]
        body = ''.join(e for e in body if e.isalnum())
        body_type_list = self.body_type.keys()
        if body!="":
            ch = process.extract(body, body_type_list, limit=2)
            if ch[0][1] > 90:
                item["autodata_bodystyle_id"] = self.body_type[ch[0][0]]
                item["autodata_bodystyle"] = ch[0][0]
        
        trans = item["transmission"]
        trans = ''.join(e for e in trans if e.isalnum())
        transmission_list = self.transmission.keys()
        if trans!="":
            ch = process.extract(trans, transmission_list, limit=2)
            if ch[0][1] > 90:
                item["autodata_transmission_id"] = self.transmission[ch[0][0]]
                item["autodata_transmission"] = ch[0][0]
        make = item["Make"]
        model = item["model"].upper()
        item["Spec"] = item['Spec'].replace(body,'')
        spec = item["Spec"].upper()
        combine = (item['Car_Name'].lower()).replace(make.lower(),'').replace(item['Year'],'').strip().upper()
        combine_list = []
        tlist = list(zip(*self.lis))
        make_list = list(dict.fromkeys(tlist[1]))
        if make!="":
            ch = process.extract(make, make_list, limit=2)
            if ch[0][1] > 90:
                item["autodata_Make_id"] = self.make_[ch[0][0]]
                item["autodata_Make"] = ch[0][0]
                index = tlist[1].index(item["autodata_Make"])
                lindex = len(tlist[1])-1-tlist[1][::-1].index(item["autodata_Make"])
                model_ = dict(zip(tlist[3][index:lindex+1], tlist[2][index:lindex+1]))
                if model !='':
                    index = tlist[1].index(item["autodata_Make"])
                    lindex = len(tlist[1])-1-tlist[1][::-1].index(item["autodata_Make"])
                    model_list = list(dict.fromkeys(tlist[3][index:lindex+1]))
                    ch = process.extract(model, model_list, limit=2)
                    if ch[0][1] > 90:
                        item["autodata_model_id"] = model_[ch[0][0]]
                        item["autodata_model"] = ch[0][0]
                        spec_index = tlist[3].index(item["autodata_model"], index, lindex+1)
                        spec_lindex = len(tlist[3])-tlist[3][::-1].index(item["autodata_model"], len(tlist[3])-lindex-1, len(tlist[3])-index)
                        spec_list = list(dict.fromkeys(tlist[5][spec_index:spec_lindex+1]))
                        spec_ = dict(zip(tlist[5][spec_index:spec_lindex+1], tlist[4][spec_index:spec_lindex+1]))
                        if spec != '':
                            ch = process.extract(spec, spec_list, limit=2)
                            if ch[0][1] > 90:
                                item["autodata_Spec"] = ch[0][0]
                                item["autodata_Spec_id"] = spec_[item["autodata_Spec"]]
                        if item["autodata_Spec"] == '':
                            for i in range(index, lindex+1):
                                combine_list.append(tlist[3][i] + '@' + tlist[5][i])
                            ch = process.extract(combine, combine_list, limit=2)
                            if(ch[0][1] > 95):
                                if ch[0][0].split('@')[1] not in item["autodata_model"]:
                                    
                                    item['autodata_Spec'] = ch[0][0].split('@')[1]
                                    item["autodata_Spec_id"] = spec_[item['autodata_Spec']]
                        
                if item["autodata_model"] == '':
                    for i in range(index, lindex+1):
                        combine_list.append(tlist[3][i] + '@' + tlist[5][i])
                    print(combine)
                    ch = process.extract(combine, combine_list, limit=2)
                    print(ch[0][1])
                    if(ch[0][1] > 90):
                        item['autodata_model'] = ch[0][0].split('@')[0]
                        item["autodata_model_id"] = model_[item['autodata_model']]
                        
                        spec_index = tlist[3].index(item["autodata_model"], index, lindex+1)
                        spec_lindex = len(tlist[3])-tlist[3][::-1].index(item["autodata_model"], len(tlist[3])-lindex-1, len(tlist[3])-index)
                        spec_list = list(dict.fromkeys(tlist[5][spec_index:spec_lindex+1]))
                        spec_ = dict(zip(tlist[5][spec_index:spec_lindex+1], tlist[4][spec_index:spec_lindex+1]))
                        item['autodata_Spec'] = ch[0][0].split('@')[1]
                        item["autodata_Spec_id"] = spec_[item['autodata_Spec']]
        return item
