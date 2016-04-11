import urllib2, json, string, base64, re, sys

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
	
def evaluate_recipe(recipe):
	recipeName = recipe['name'].encode('ascii','ignore')
	recipeTime = str(recipe['totalTimeInSeconds']).encode('ascii','ignore')
	numIngredients = str(len(recipe['ingredientLines'])).encode('ascii','ignore')
	flavors = recipe['flavors']

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

	queryTextFile = argv[0]
	f = open(queryTextFile)
	query = f.read().lower()
	
	query = "'%s'" % query
	urlQuery = 'q=' + replace_chars(query)
	searchParamenters = urlQuery
	
	url = 'http://api.yummly.com/v1/api/recipes?%s&%s' % (yummlyCredentials, searchParamenters)
	results = process_request(url)
	
	comlpeteRecipes = []
	for item in results["matches"]:
		#print item['id']
		comlpeteRecipes.append(get_recipe(item['id'], yummlyCredentials))
		
	recipeDetails = []
	for item in comlpeteRecipes:
		recipeDetails.append(evaluate_recipe(item))
	
	for detail in recipeDetails:
		print detail
	
	scored_recipes.sort(key=lambda number: number[-1])

	printResults(query)
	
	#print results
	
if __name__ == '__main__':
	main(sys.argv[1:]) # ignores passing the file named
