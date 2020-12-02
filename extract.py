from bs4 import BeautifulSoup
from multiprocessing import Pool

def extract(ind):
	try:
		with open("DONs/{}.html".format(ind)) as f:
			htmldoc = f.read()
		soup = BeautifulSoup(htmldoc, "lxml")
		div_primary = soup.select_one("#primary")
		with open("Extracted/{}.html".format(ind), "w") as f:
			f.write(str(div_primary))
		return 0
	except:
		return -1

pool = Pool(4)
pool.map(extract, range(2898))