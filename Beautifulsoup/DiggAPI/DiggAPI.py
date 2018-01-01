"""
December 31 2017
Uses bs4 to scrape Digg.com/technology for top technolgoy news stories and returns
the links and titles of the corresponding pages as a JSON dump.
"""

import bs4
import requests
import json
from flask import Flask

def get_news():
    index_url = "http://digg.com/channel/technology"
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    generaldata = soup.find_all("div" , {"class" : "digg-story__content"})
    data = []
    for story in generaldata:
        title = story.find_all("h2", {"itemprop" : "headline"})[0].text
        #print(story.find_all(re.compile("h2"))[0].text) #Does the same thing as above but with re
        for link in story.find_all('a', href = True):
            url = link['href']
        data.append({"Title :" : title.replace("\n", ""), "Link : " : url.replace("\n", "")})
    return json.dumps(data)

app = Flask(__name__)
@app.route('/technology', methods = ['GET'])
def technology():
    return get_news()

if __name__ == '__main__':
    print(technology())

