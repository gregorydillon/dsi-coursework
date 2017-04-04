from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests

client = MongoClient()
# Access/Initiate Database
db = client['test_database']
# Access/Initiate Table
tab = db['test_table']

def part_one():
    # class = sresult
    content = ''
    with open('data/ebay_shoes.html') as ebay_html:
        print ebay_html
        ebay_str = ebay_html.readlines()
        content = content.join(ebay_str)

    soup = BeautifulSoup(content, 'html.parser')
    images = soup.select('img.img')
    image_sources = [image_tag['src'] for image_tag in images]

    for image in image_sources:
        f = 'images/' + image.split('/')[-1]
        urlretrieve('file://' + os.getcwd() + '/data/' + image, filename=f)

def fetch_ebay_images(ebay_search_url):
    r = requests.get(ebay_search_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    images = soup.select('img.img')
    image_sources = [image_tag['src'] for image_tag in images]

    for image in image_sources:
        f = 'images/' + image.split('/')[-2] + '.jpg'
        print image, f
        urlretrieve(image, filename=f)
