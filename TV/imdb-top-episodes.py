import requests
from bs4 import BeautifulSoup
import os.path
import pprint
import time

file_path = "cache\imdb.html"
fileDir = os.path.dirname(os.path.realpath('__file__')) #<-- absolute dir the script is in
abs_file_path = os.path.join(fileDir, file_path)
page_size = 50
num_votes = 2000
URL = "https://www.imdb.com/search/title/?title_type=tv_episode&num_votes={},&sort=user_rating,desc&ref_=adv_prev".format(num_votes)
content = None
pp = pprint.PrettyPrinter(indent=4)

# read it back in
if os.path.isfile(abs_file_path) and os.path.getsize(abs_file_path) > 0:
    with open(abs_file_path) as f:
        filecontent = f.read()
        content = filecontent.encode()

if content is None:
    with open(abs_file_path, "w") as f:
        page = requests.get(URL)
        f.write(page.content.decode())
        content = page.content

soup = BeautifulSoup(content, 'html.parser')
results = soup.find_all("div", {"class": "lister-item mode-advanced"})
seriesDictionary = {}

for result in results:
    content = result.find('div', class_='lister-item-content')
    header = content.find('h3', class_='lister-item-header')
    title = header.find('a')
    if title.text in seriesDictionary:
        seriesDictionary[title.text] += 1
    else:
        seriesDictionary[title.text] = 1

sortedDict = sorted(seriesDictionary.items(), key = lambda kv: kv[1], reverse=True)
pp.pprint(sortedDict)