import logging

from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime


def main():
    logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQipdjO8QWhilhhJ4bX0FBebnHEzK1G3LEDQbE_S-xRvs2t0oHNm--acHwMRFmL9uKw4cXcOUqy1V66/pubhtml"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    table = soup.find_all("table")[0]

    logging.info("Received Colorado Data", exc_info=False);

    with open("out/CO_" + datetime.now().strftime('%Y%m%d') + ".csv", "w") as f:
        csv_writer = csv.writer(f)
        index = 0
        for row in table.find_all("tr"):
            if index > 8 and index != 10:
                csv_writer.writerows([[td.text for td in row.find_all("td")]])
            index = index + 1
    logging.info("Wrote Colorado Data", exc_info=False);

#main()
