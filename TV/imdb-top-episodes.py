import requests
from bs4 import BeautifulSoup
import os.path
import pprint
import time

file_ext = ".html"
fileDir = os.path.dirname(os.path.realpath('__file__')) #<-- absolute dir the script is in
abs_file_path = os.path.join(fileDir, "cache\imdb")
pp = pprint.PrettyPrinter(indent=4)
seriesDictionary = {}
num_votes = 2000
URL = "https://www.imdb.com/search/title/?title_type=tv_episode&num_votes={},&sort=user_rating,desc&ref_=adv_prev".format(num_votes)

sleep_timer = 10
page_size = 50
number_of_pages = 20

for i in range(number_of_pages):
    content = None
    pageURL = URL + "&start={}".format(page_size*i+1)
    current_file = abs_file_path + str(i+1) + file_ext

    if os.path.isfile(current_file) and os.path.getsize(current_file) > 0:
        with open(current_file) as f:
            filecontent = f.read()
            content = filecontent.encode()

    if content is None:
        with open(current_file, "w") as f:
            print("Please wait. Fetching next {} results...".format(page_size))
            time.sleep(sleep_timer)
            page = requests.get(pageURL)
            f.write(page.content.decode())
            content = page.content

    soup = BeautifulSoup(content, 'html.parser')
    results = soup.find_all("div", {"class": "lister-item mode-advanced"})

    for result in results:
        content = result.find('div', class_='lister-item-content')
        header = content.find('h3', class_='lister-item-header')
        show = header.find('a').text.strip()
        if show in seriesDictionary:
            seriesDictionary[show] += 1
        else:
            seriesDictionary[show] = 1
    print("Found {} shows in total!".format(len(seriesDictionary)))

sortedDict = sorted(seriesDictionary.items(), key = lambda kv: kv[1], reverse=True)
pp.pprint(sortedDict)