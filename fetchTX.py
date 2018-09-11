from bs4 import BeautifulSoup
import requests
import os, os.path, csv, re, time

class FetchTX():

	def __init__(self):
		self.listingurl = "https://etherscan.io/txsPending?ps=100&p=1&sort=LastSeen&order=desc"
		self.response = requests.get(self.listingurl)
		self.soup = BeautifulSoup(self.response.text, 'html.parser')

	def getPendingTx(self):
		data = []
		for tr in self.soup.findAll('table')[0].findAll('tr')[1:]:
			timestamp = tr.find_all('td')[2].get_text()
			if 'sec' in timestamp:
				timestamp = int(time.time()) - int(re.search(r'\d+', timestamp).group(0))
				gasLimit = tr.find_all("td")[3].get_text()
				gasPrice = tr.find_all("td")[4].get_text().replace(' Gwei', '')
				address = tr.find("span", class_="address-tag").a.get_text()
				data.append([address, timestamp, gasLimit, gasPrice])
			else:
				print(timestamp)
		return data
