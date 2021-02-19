# add all imports here
import csv
import json
import urllib
from _csv import reader

import pandas as pd
from datetime import date

import requests


def main():
    to_csv()
    copy_to_main()


def to_csv():
    df = pd.DataFrame(columns=['school id', 'name', 'address1', 'address2', 'city', 'zipcode', 'phone', 'website',
                               'latitude', 'longitude', 'last updated', 'opening date', 'operating type id',
                               'operating type', 'region id', 'region name', 'region contact', 'region phone',
                               'region zipcode', 'student cases', 'staff cases', 'last week student cases',
                               'last week staff cases', 'date scraped'])
    url = "https://districtinformation.tnedu.gov/api/districts"
    open_url = urllib.request.urlopen(url)
    json_data = json.loads(open_url.read())
    for sd in json_data:
        school_id = sd["id"]
        name = sd["name"]
        address1 = sd["address1"]
        address2 = sd["address2"]
        city = sd["city"]
        zipcode = sd["zip"]
        phone = sd["phone"]
        website = sd["website"]
        lat = sd["latitude"]
        long = sd["longitude"]

        operating_model = sd["districtOperatingModel"]
        last_updated = operating_model["lastUpdatedDate"]
        school_opening_date = operating_model["schoolOpeningDate"]
        operating_type_id = operating_model["operatingModel"]["id"]
        operating_type = operating_model["operatingModel"]["name"]

        region = sd["region"]
        region_id = region["id"]
        region_name = region["name"]
        region_contact_name = region["contactName"]
        region_phone = region["phone"]
        region_zip = region["zip"]

        covid_data = sd["covidData"]
        student_cases = covid_data["studentCases"]
        staff_cases = covid_data["staffCases"]
        last_week_student_cases = covid_data["lastWeekStudentCases"]
        last_week_staff_cases = covid_data["lastWeekStaffCases"]

        new_row = pd.Series(data={'school id': school_id, 'name': name, 'address1': address1, 'address2': address2,
                                  'city': city, 'zipcode': zipcode, 'phone': phone, 'website': website,
                                  'latitude': lat, 'longitude': long, 'last updated': last_updated,
                                  'opening date': school_opening_date, 'operating type id': operating_type_id,
                                  'operating type': operating_type, 'region id': region_id, 'region name': region_name,
                                  'region contact': region_contact_name, 'region phone': region_phone,
                                  'region zipcode': region_zip, 'student cases': student_cases,
                                  'staff cases': staff_cases,
                                  'last week student cases': last_week_student_cases,
                                  'last week staff cases': last_week_staff_cases, 'date scraped': date.today()})
        df = df.append(new_row, ignore_index=True)
    # writes to "Tennessee.csv" file
    df.to_csv('Tennessee.csv', index=False)


def copy_to_main():
    f1 = open("Tennessee.csv", 'r')
    f2 = open('SchoolDistricts.csv', 'a')
    csv_reader = reader(f1)
    csv_writer = csv.writer(f2)
    isFirst = True;
    for row in csv_reader:
        if isFirst:
            isFirst = False
        else:
            address = row[2] + ", " + row[4] + ", " + row[5]
            csv_writer.writerow(["Tennessee", row[1], row[13], address, row[8], row[9], row[10]])
    f1.close()
    f2.close()


main()
