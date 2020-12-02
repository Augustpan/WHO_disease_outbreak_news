from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import pandas as pd
import requests
from os.path import exists

def download(url, target):
	with open(target, "wb") as writer:
		writer.write(requests.get(url).content)

# retrieve archive by year
with ThreadPoolExecutor(8) as executor:
	for year in range(1996, 2021):
		if not exists("DONs_archive/WHO_DONs_{}.html".format(year)):
			executor.submit(download, "https://www.who.int/csr/don/archive/year/{}/en/".format(year), "DONs_archive/WHO_DONs_{}.html".format(year))

list_href = []
list_date = []
list_info = []

for year in range(1996, 2021):
	with open("DONs_archive/WHO_DONs_{}.html".format(year)) as f:
		htmldoc = f.read()

	soup = BeautifulSoup(htmldoc, "lxml")

	selected_li = soup.select("ul.auto_archive > li")
	for tag_li in selected_li:
		tag_a = tag_li.select_one("a")
		tag_span = tag_li.select_one("span")
		
		href = "https://www.who.int" + tag_a["href"]
		date = tag_a.string
		info = tag_span.string

		list_href.append(href)
		list_date.append(date)
		list_info.append(info)

df = pd.DataFrame({"href":list_href, "date":list_date, "info":list_info})
df.to_csv("save.csv")

# retrieve DONs
with ThreadPoolExecutor(8) as executor:
	for ind, url in enumerate(df.href):
		if not exists("DONs/{}.html".format(ind)):
			executor.submit(download, url, "DONs/{}.html".format(ind))