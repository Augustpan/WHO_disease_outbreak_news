from bs4 import BeautifulSoup
from multiprocessing import Pool

def proc(ind):
	try:
		with open("Extracted/{}.html".format(ind)) as f:
			htmldoc = f.read()
		soup = BeautifulSoup(htmldoc, "lxml")
		doc = soup.get_text()
		with open("Transformed/{}.txt".format(ind), "w") as f:
			f.write(doc)
		return 0
	except:
		return -1

pool = Pool(4)
pool.map(proc, range(2898))