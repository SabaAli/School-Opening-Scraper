#add all imports here
import json
import urllib
import pandas as pd
from datetime import date

import requests

def main():
    to_csv()

def to_csv():
    df = pd.DataFrame(columns=['school','alt name','address','instructional delivery','week of','total positive cases','date scraped'])
    url = "https://services7.arcgis.com/4RQmZZ0yaZkGR1zy/arcgis/rest/services/alsde_c19_publish_PUBLIC/FeatureServer/0/query?f=json&where=WeekOf%3D7&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=SchoolSystem%20asc&outSR=102100&resultOffset=0&resultRecordCount=200&resultType=standard&cacheHint=true"
    openUrl = urllib.request.urlopen(url)
    jsonD = json.loads(openUrl.read())
    for p in jsonD["features"]:
        school_system = p["attributes"]["SchoolSystem"]
        alt_name = p["attributes"]["AltName"]
        address = p["attributes"]["Address"]
        instructional_delivery = p["attributes"]["InstructionalDelivery"]
        week_of = p["attributes"]["WeekOf"]
        total_pos_lbl = p["attributes"]["TotalPositive_lbl"]
        new_row = pd.Series(data={'school':school_system, 'alt name':alt_name, 'address':address,
                                  'instructional delivery':instructional_delivery, 'week of':week_of,
                                  'total positive cases':total_pos_lbl,'date scraped':date.today()})
        df = df.append(new_row, ignore_index=True)
    df.to_csv('Alabama.csv',index=False)

main()