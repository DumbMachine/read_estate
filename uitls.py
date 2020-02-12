from bs4 import BeautifulSoup as soup

def read_attribute(soup_object, attribute):
    return [text.text.strip() for text in soup_object.select(attribute)]

def read_amenities(soup_object):
    attr = "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div:nth-child(4) > div.property-page__description"
    things = read_attribute(soup_object, attr)

'''
# TODO: Remove the personal detials and things that might not be required for analysis
# TODO: Make FEATURES, ismorgaguge, and others
'''
def read_description(soup_object):
    attr = "body > main > div > div > div.container > div.property-page__column > div.property-page__column--left > div:nth-child(4) > div.property-page__description"
    things = read_attribute(soup_object, attr)
    return things
