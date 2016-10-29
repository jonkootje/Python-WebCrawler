import os
from bs4 import BeautifulSoup
import requests
# import pyping

links = []
count = 0
successrate = 0

def init():
	global links
	global count

	url = input('Starter url: ') # Where it all starts
	try:
		html = requests.get(url).text
	except:
		print('[ERROR] Could not connect to host ' + url + '.\n- Please run script with admin rights\n- Check if host is online and if pc is online.')
		exit()
	soup = BeautifulSoup(html, "html.parser")
	for a in soup.find_all('a', href=True):
		
		if (a['href'] not in links):
			if ('mailto:' not in a['href']):
				links.append(a['href'])

	print(links)
	startLoop()

def startLoop():
	global links
	global count
	global successrate

	while (count <= len(links) - 1):
		url = links[count]
		if "http" in url:
			try:
				html = requests.get(url).text
			except:
				print('[ERROR] Could not connect to: ' + url)
			else:
				successrate += 1
				soup = BeautifulSoup(html, "html.parser")
				for a in soup.find_all('a', href=True):
					if (a['href'] not in links):
						if ('mailto:' not in a['href']):
							links.append(a['href'])
			
				print('[SUCCESS (' + str(successrate) +' / ' + str(count) +')] Connected to: ' + url)
		count += 1
	print('END OF LIST')
	return True

def mergeUrl(data):

	if (data['url'][0:1] == '/'):
		# goto root
		b = data['from'].split('.')[len(data['from'].split('.')) - 1]
		if ("/" not in b):
			# from is in root so just combine the 2 variables
			return data['from'] + data['url']
		else:
			remove = b.split('/', 1)[b.split('/') - 1]
			return data['from'].replace(remove, '') + data['url']
			# from is not in root
	else:
		# dont goto root
		if (data['from'][len(data['from'])-1] == '/'):
			# dont have to add /
			return data['from'] + data['url']
		else:
			return data['from'] + '/' + data['url']


init()
