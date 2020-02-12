import time
from tqdm import tqdm
import os
import pickle
import requests
import pandas as pd
from glob import glob
from utils import *
from bs4 import BeautifulSoup as soup

link = "https://www.propertyfinder.ae/en/buy/apartment-for-sale-dubai-jumeirah-beach-residence-shams-shams-4-7304200.html"

class HouseDetails:
    """Short summary."""
    def __init__(self, url):
        """Initailise the house object.

        Parameters
        ----------
        url : string
            the url from the dubai properties Website

        """
        self.url = url
        self.content = None
        self.details = {
            "title_advert": None,
            "location1": None,
            "location2": None,

            "property_type": None,
            "property_size": None,

            "bedrooms": None,
            "bathrooms": None,

            "cost": None,
            "amenities": None,
            "description": None,

            "listed": None
        }

    def get_content(self):
        """Downloads thepage and stores in a soup variable.

        Returns
        -------
        type
            Description of returned object.

        """
        req = requests.get(
            self.url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        )
        if req.status_code == 200:
            self.content = soup(req.text, "lxml")
        else:
            print(req.status_code)
            raise Exception("Something wrong when requesting for data from the page")

    def scrape(self):
        """Get the important information.

        Returns
        -------
        type
            Description of returned object.

        """
        try:
            title_advert = read_attribute(self.content, "h1.text")
            self.details['title_advert'] = title_advert
        except Exception as e:
            print(e)

        try:
            property_type = read_attribute(self.content, "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div.panel.panel--style1.panel--style3 > div > div:nth-child(1) > div:nth-child(1) > div.text.text--bold.property-facts__content")
            self.details['property_type'] = property_type
        except Exception as e:
            print(e)
        try:
            property_size = read_attribute(self.content, "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div.panel.panel--style1.panel--style3 > div > div:nth-child(1) > div:nth-child(2) > div.text.text--bold.property-facts__content")
            self.details['property_size'] = property_size
        except Exception as e:
            print(e)

        try:
            completion = read_attribute(self.content, "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div.panel.panel--style1.panel--style3 > div > div:nth-child(1) > div:nth-child(3) > div.text.text--bold.property-facts__content")
            self.details['completion'] = completion
        except Exception as e:
            print(e)

        try:
            bedrooms = read_attribute(self.content, "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div.panel.panel--style1.panel--style3 > div > div:nth-child(2) > div:nth-child(1) > div.text.text--bold.property-facts__content")
            self.details['bedrooms'] = bedrooms
        except Exception as e:
            print(e)
        try:
            bathrooms = read_attribute(self.content, "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div.panel.panel--style1.panel--style3 > div > div:nth-child(2) > div:nth-child(2) > div.text.text--bold.property-facts__content")
            self.details['bathrooms'] = bathrooms
        except Exception as e:
            print(e)

        try:
            # cost = read_attribute(self.content, "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div:nth-child(2) > div > div > div.property-page__contact-section-column > div.property-page__contact-section--left-area > div.property-price > div > div > div")
            cost = read_attribute(self.content, "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div:nth-child(2) > div > div > div.property-page__contact-section-column > div.property-page__contact-section--left-area > div.property-price")
            self.details['cost'] = cost
        except Exception as e:
            print(e)
        try:
            location1 = read_attribute(self.content, "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div:nth-child(3) > div > div.property-location > div > div.property-location__detail-area")
            self.details['location1'] = location1
        except Exception as e:
            print(e)
        try:
            amenities = read_amenities(self.content)
            self.details['amenities'] = amenities
        except Exception as e:
            print(e)

        try:
            descriptions = read_description(self.content)
            self.details['descriptions'] = descriptions
        except Exception as e:
            print(e)

        try:
            listed = read_attribute(self.content, "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div:nth-child(4) > div.property-page__legal-list-area > div.property-page__legal-left-area > div:nth-child(3)")
            self.details['listed'] = listed
        except Exception as e:
            print(e)

        return self.details

files = sorted(glob("links/propertyfinder*.pkl"))
# files = glob("*.pkl")
with tqdm(total=len(files)) as progress:
    for file in files:
        progress.set_description(file)
        progress.update(1)
        local_itr = 0
        if not os.path.isfile(f"csvs/{file.replace('pkl', 'csv').replace('links/','')}"):
            houses = []
            links = pickle.load(open(file, "rb"))
            for link in links:
                local_itr+=1
                time.sleep(8)
                something = HouseDetails(link)
                something.get_content()
                houses.append(something.scrape())
                progress.set_description(file+ "--"+ str(local_itr))
                # Have used this i/o wastage on purpose
                pd.DataFrame(houses).to_csv(f"csvs/{file.replace('pkl', 'csv').replace('links/','')}")
