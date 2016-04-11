import urllib2, json, string, base64, re, sys
from bs4 import BeautifulSoup

scored_recipes = []

def replace_chars(query):
	query = string.replace(query, "'", '%27')
	query = string.replace(query, '"', '%27')
	query = string.replace(query, '+', '%2b')
	query = string.replace(query, ' ', '%20')
	query = string.replace(query, ':', '%3a')
	query = string.replace(query, '(', '%28')
	query = string.replace(query, ')', '%29')
	query = string.replace(query, '[', '%5b')
	query = string.replace(query, ']', '%5d')
	return query
	
def process_request(url):
	request = urllib2.Request(url)
	requestOpener = urllib2.build_opener()
	response = requestOpener.open(request)
	results = json.load(response)
	return results

def get_recipe(recipeID, yummlyCredentials):
	recipeURL = 'http://api.yummly.com/v1/api/recipe/%s?%s' % (recipeID, yummlyCredentials)
	recipeInfo = process_request(recipeURL)
	return recipeInfo

# currently only works with recipes taken from foodnetwork.com
def get_directions(url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")

	direction_soup = soup.find_all(itemprop='recipeInstructions')[0].p
	directions = direction_soup.get_text() + "\n"
	siblings = direction_soup.find_next_siblings("p")
	siblings = siblings[:-2]

	for sibling in siblings:
		directions += sibling.get_text() + "\n"

	return directions
	
def evaluate_recipe(recipe):
	recipeName = recipe['name'].encode('ascii','ignore')
	recipeTime = str(recipe['totalTimeInSeconds']).encode('ascii','ignore')
	numIngredients = str(len(recipe['ingredientLines'])).encode('ascii','ignore')
	flavors = recipe['flavors']
	sourceDict = recipe['source']
	sourceName = sourceDict['sourceDisplayName'].encode('ascii','ignore')
	print sourceName
	directions = ""

	# currently, only Food Network sources work. 
	if "Food Network" in sourceName:
		directions = get_directions(sourceDict['sourceRecipeUrl'])
		print directions

	scored_recipes.append((recipeName,evaluate_simplicity(numIngredients,recipeTime)))

	importantInfo = "The recipe " + recipeName + " has " + numIngredients + " ingredients and takes " + recipeTime + " seconds to make."
	return importantInfo 

def evaluate_simplicity(numIng, recipeTime):
	alpha = 0.6
	beta = 0.001

	return alpha*int(numIng) + beta*int(recipeTime)

def printResults(query):
	print 'The simplest recipes for the query ' + query + ' is the following:'
	i = 0
	while i < len(scored_recipes):
		print str(i+1) + '. ' + str(scored_recipes[i])
		i += 1
	
def main(argv):
	#credentials structure: _app_id=app-id&_app_key=app-key
	yummlyAppID = "1a10b2e0"
	yummlyAppKey = "72595b3dee46471a8a93caa35baf8ef1"
	yummlyCredentials = '%s=%s&%s=%s' % ('_app_id', yummlyAppID, '_app_key', yummlyAppKey)

	#queryTextFile = argv[0]
	#f = open(queryTextFile)
	#query = f.read().lower()
	query = ''
	
	query = "'%s'" % query
	#urlQuery = 'q=' + replace_chars(query)
	urlQuery = "q=Food+Network"
	allowedIngredients = ['chicken']
	urlIngredients = ''
	for ing in allowedIngredients:
		urlIngredients = urlIngredients + '&allowedIngredient[]=%s' % ing

	recipeSource = "&allowedSource=Food+Network"

	searchParamenters = urlQuery + urlIngredients + recipeSource
	#print searchParamenters
	
	url = 'http://api.yummly.com/v1/api/recipes?%s&%s' % (yummlyCredentials, searchParamenters)
	results = process_request(url)
	
	completeRecipes = []
	for item in results["matches"]:
		#print item['id']
		completeRecipes.append(get_recipe(item['id'], yummlyCredentials))
		
	recipeDetails = []
	for item in completeRecipes:
		recipeDetails.append(evaluate_recipe(item))
	
	for detail in recipeDetails:
		print detail
	
	scored_recipes.sort(key=lambda number: number[-1])

	printResults(query)
	
	#print results
	
if __name__ == '__main__':
	main(sys.argv[1:]) # ignores passing the file named
