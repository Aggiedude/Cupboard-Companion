# part1.py - Takes advantage of urllib in order to call the Bing Search API.
# It then stores the "Title" and "Description" of each web page returned and stores them
# in a folder called "Data" as doc1, doc2, etc. 
# usage: python part1.py
# Andrew Chepey
import urllib2, base64, json, re, os

BING_KEY = '20Te5NY5OKBOMmg1iZvjyDnVBYzAvcpi8pCUtanAm0A'
username = 'user'
numDocs = 0

def parseDocs(s):
	global numDocs

	data = json.loads(s)
	documents = data["results"]
	print documents

	# Handles the creation of the data folder for necessary files
	if not os.path.exists('./Data'):
		os.makedirs('Data')

	for doc in documents:
		f = open(os.getcwd()+'/Data/doc%03d.txt' % numDocs, 'w')
		
		# replaces punctuation and non character data with spaces in order to avoid encoding errors. 
		f.write(re.sub(r'\W+', ' ', doc["title"])+'\n'+re.sub(r'\W+', ' ', doc["description"]))
		numDocs += 1		

def bingAPIcall(query):
	httpQuery = str(query.replace(' ','%20').lower())
	urlQuery = 'http://www.recipepuppy.com/api/?i=' + httpQuery
	request = urllib2.Request(urlQuery)
	# encodedPass = base64.encodestring(username + ":" + BING_KEY).replace('\n','')
	# request.add_header("Authorization", "Basic " + encodedPass)
	return urllib2.urlopen(request).read().lower()

def main():
	# bread butter cheese
	parseDocs(bingAPIcall('bread,butter,cheese'))

if __name__ == '__main__':
	main()