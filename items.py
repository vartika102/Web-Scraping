# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MetaItem(scrapy.Item):
    src = scrapy.Field()
    ts = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    uid = scrapy.Field()
    cs = scrapy.Field()

class AutodataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Last_Code_Update_Date = scrapy.Field()  #Monday, April 29, 2019
    Scrapping_Date = scrapy.Field()  #Monday, April 29, 2019
    Source = scrapy.Field()
    Country = scrapy.Field() #UAE
    City = scrapy.Field() #Sharjah
    Seller_Type = scrapy.Field() #Large independent dealers
    Seller_Name = scrapy.Field() #automalluae
    Car_URL = scrapy.Field() #https://www.automalluae.com/used-car-shop/9538886-toyota-prius-iconic/
    Car_Name = scrapy.Field() #Toyota Prius ICONIC
    Year = scrapy.Field() #2017
    Make = scrapy.Field() #Toyota
    model = scrapy.Field() #Prius
    Spec = scrapy.Field() #ICONIC
    Doors = scrapy.Field() #5
    transmission = scrapy.Field() #Automatic
    trim = scrapy.Field() #Grey - Leather
    bodystyle = scrapy.Field() #Hatchback
    other_specs_gearbox = scrapy.Field() #
    other_specs_seats = scrapy.Field()
    other_specs_engine_size = scrapy.Field() #1.8l
    other_specs_horse_power = scrapy.Field() 
    colour_exterior = scrapy.Field() #Silver
    colour_interior = scrapy.Field() 
    fuel_type = scrapy.Field() #Diesel
    import_yes_no_also_referred_to_as_GCC_spec = scrapy.Field() 
    mileage = scrapy.Field() #55924
    condition = scrapy.Field()
    warranty_untill_when = scrapy.Field()
    service_contract_untill_when = scrapy.Field()
    Price_Currency = scrapy.Field()
    asking_price_inc_VAT = scrapy.Field()
    asking_price_ex_VAT = scrapy.Field() #69956
    warranty = scrapy.Field() #Yes
    service_contract = scrapy.Field()
    vat = scrapy.Field() #Yes
    mileage_unit = scrapy.Field()
    engine_unit = scrapy.Field()
    meta = scrapy.Field()
    autodata_transmission = scrapy.Field()
    autodata_transmission_id = scrapy.Field()
    autodata_bodystyle = scrapy.Field()
    autodata_bodystyle_id = scrapy.Field()
    autodata_Make = scrapy.Field()
    autodata_Make_id = scrapy.Field()
    autodata_model = scrapy.Field()
    autodata_model_id = scrapy.Field()
    autodata_Spec = scrapy.Field()
    autodata_Spec_id = scrapy.Field()
    wheel_size = scrapy.Field()
    top_speed_kph = scrapy.Field()
    cylinders = scrapy.Field()
    torque_Nm = scrapy.Field()
    acceleration = scrapy.Field()
