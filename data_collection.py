import urllib2, json, string, base64, re, sys
from bs4 import BeautifulSoup
from textstat.textstat import textstat

scored_recipes = []
ingrList = []

# replaces common characters in URL queries with appropriately formatted characters
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

# uses the urllib function to grab the response to a HTTP GET request
def process_request(url):
	request = urllib2.Request(url)
	requestOpener = urllib2.build_opener()
	response = requestOpener.open(request)
	results = json.load(response)
	return results

# returns the approximate grade-level needed to read the text
# used the formula obtained from wikipedia
def flesch_kincaid_score(text):
	sylCount = textstat.syllable_count(text)
	wordCount = len(text.split())
	sentenceCount = textstat.sentence_count(text)

	print "Syl count - %s, word count - %s, sentenceCount - %s " % (sylCount,wordCount,sentenceCount)

	return (0.39*(wordCount/sentenceCount)+11.8*(sylCount/wordCount) - 15.59)

def num_on_hand

# Calls the Yummly API to get details of a specific recipe
def get_recipe(recipeID, yummlyCredentials):
	recipeURL = 'http://api.yummly.com/v1/api/recipe/%s?%s' % (recipeID, yummlyCredentials)
	recipeInfo = process_request(recipeURL)
	return recipeInfo

# Scrapes the source HTML page gathered from the yummly api for recipe directions 
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

# main algorithm for project
# Extracts all necessary data from the yummly api, and calls the simplicity algorithm
def evaluate_recipe(recipe):
	recipeName = recipe['name'].encode('ascii','ignore')
	print "evaluating %s" % recipeName
	
	prepTime = 0
	if 'prepTimeInSeconds' in recipe:
		prepTime = recipe['prepTimeInSeconds']

	cookTime = 0
	if 'cookTimeInSeconds' in recipe:
		cookTime = recipe['cookTimeInSeconds']
	else:
		if prepTime == 0: # API returned non-specific cooking time
			cookTime = recipe['totalTimeInSeconds'] # will use total time as cook time in algorithm instead

	numIngredients = len(recipe['ingredientLines'])
	flavors = recipe['flavors']

	sourceDict = recipe['source']
	sourceName = sourceDict['sourceDisplayName'].encode('ascii','ignore')
	directionsText = ""

	# currently, only Food Network sources work. 
	if "Food Network" in sourceName:
		directionsText = get_directions(sourceDict['sourceRecipeUrl'])
		print directionsText

	if directionsText:
		simplicityScore = evaluate_simplicity(numIngredients,prepTime,cookTime,directionsText)
		scored_recipes.append((recipeName,simplicityScore))

# Assigns a score to a recipe based upon a number of factors 
def evaluate_simplicity(numIng, prepTime, cookTime, directionsText):
	numIngConst = 0.6
	prepConst = 0.002
	cookConst = 0.001
	fkConst = 0.5
	stepsConst = 0.3
	notOnHandConst = 2.0

	fkScore = flesch_kincaid_score(directionsText)
	numSteps = len([s.strip() for s in directionsText.splitlines()])


	return numIngConst*numIng + prepConst*prepTime + cookConst*cookTime + fkConst*fkScore + stepsConst*numSteps

def printResults(ingList):
	print 'The simplest recipes for the ingredients ' + str(ingList) + ' is the following:'
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
	ingrList = f.read().lower().split()

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
		
	# evaluate the simplicity for every recipe gathered
	for item in completeRecipes:
		evaluate_recipe(item)
	
	scored_recipes.sort(key=lambda number: number[-1])

	printResults(ingrList)
	
	#print results
	
if __name__ == '__main__':
	main(sys.argv[1:]) # ignores passing the file named
