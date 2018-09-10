from bs4 import BeautifulSoup
import requests
import os, os.path, csv, re, time

listingurl = "https://etherscan.io/txsPending"
response = requests.get(listingurl)
soup = BeautifulSoup(response.text, "html.parser")

for tr in soup.findAll('table')[0].findAll('tr')[1:20]:
	timestamp = tr.find_all("td")[2].get_text()
	if 'sec' in timestamp:
		timestamp = int(time.time()) - int(re.search(r'\d+',timestamp).group(0))
		gasLimit = tr.find_all("td")[3].get_text()
		gasPrice = tr.find_all("td")[4].get_text()
		name = tr.find("span", class_="address-tag").a.get_text()
		print(name, timestamp, gasLimit, gasPrice)

