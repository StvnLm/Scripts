import bs4
import requests
import time
index_url = "https://www.yellowpages.com/search?search_terms=coffee&geo_location_terms=new+york"
response = requests.get(index_url)
soup = bs4.BeautifulSoup(response.content, "html.parser")
generalData = soup.find_all("div", {"class":"info"})
for item in generalData:
    print(item.find_all("a", {"class":"business-name"})[0].text,
          item.find_all("span", {"itemprop":"streetAddress"})[0].text,
          item.find_all("span", {"itemprop":"addressLocality"})[0].text.replace(',', ''),
          item.find_all("span", {"itemprop":"addressRegion"})[0].text,
          item.find_all("span", {"itemprop":"postalCode"})[0].text,
          item.find_all("div", {"class":"phones phone primary"})[0].text, "\n")

