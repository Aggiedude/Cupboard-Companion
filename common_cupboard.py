import urllib2, json, string, base64, re, sys
from collections import Counter

# uses the urllib function to grab the response to a HTTP GET request
def process_request(url):
	request = urllib2.Request(url)
	requestOpener = urllib2.build_opener()
	response = requestOpener.open(request)
	results = json.load(response)
	return results

def gather_ingredients(allRecipes):
	allIngredients = []
	countedIngredients = []
	for item in allRecipes:
		for ing in item:
			allIngredients.append(ing)
	
	countedIngredients = count_ingredients(allIngredients).items()
	return countedIngredients

def count_ingredients(allIngredients):
	count = Counter()
	for ing in allIngredients:
		count[ing] += 1

	return count
	
def most_common(countedIngredients):
#gathers the five highest scoring documents
	topIngredients = []
	countedIngredients = sorted(countedIngredients,key=get_key, reverse=True)
	topIngredients = countedIngredients[:10]
	return topIngredients
	
def get_key(item):
#helper function for most_common
	return item[1]
		
def main(argv):
	#credentials structure: _app_id=app-id&_app_key=app-key
	yummlyAppID = "1a10b2e0"
	yummlyAppKey = "72595b3dee46471a8a93caa35baf8ef1"
	yummlyCredentials = '%s=%s&%s=%s' % ('_app_id', yummlyAppID, '_app_key', yummlyAppKey)
			
	urlQuery = "q="
	urlIngredients = ''

	searchParamenters = urlQuery + '&maxResult=550'
	
	url = 'http://api.yummly.com/v1/api/recipes?%s&%s' % (yummlyCredentials, searchParamenters)
	results = process_request(url)
	
	allRecipes = []
	for item in results["matches"]:
		allRecipes.append(item['ingredients'])
	
	commonCupboard = []
	commonCupboard = most_common(gather_ingredients(allRecipes))
	print commonCupboard
	
if __name__ == '__main__':
	main(sys.argv)
