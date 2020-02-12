import time
import os
import pickle
import requests
import pandas as pd9
from bs4 import BeautifulSoup as soup
from tqdm import tqdm

base = "https://www.propertyfinder.ae/en/buy/properties-for-sale.html?page={pageno}"

with tqdm(total=500) as progress:
    for page in range(1, 500):
        filename = f"propertyfinder-pagenumber-{page}.pkl"
        if not os.path.isfile(filename):
            links = []
            content = soup(requests.get(
                base.format(pageno=page),
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            ).text, 'lxml')
            time.sleep(7)
            links = [
                "https://www.propertyfinder.ae" + i.a['href'] for i in content.find_all("div", {"class": "card-list__item"})
            ]
            pickle.dump(file=open(filename, "wb"), obj=links)
        progress.update(1)
