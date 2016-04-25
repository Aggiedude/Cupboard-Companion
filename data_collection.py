import urllib2, json, string, base64, re, sys
from bs4 import BeautifulSoup
from textstat.textstat import textstat

allowedIngredients = []
mainIngredientRecipes = []
recipeList = []
commonCupboard = ['salt','egg','eggs','butter','oil','sugar','granulated sugar','pepper','garlic','milk','all-purpose flour','flour','water']

class Recipe:

	def __init__(self, name):
		self.name = name
		self.ingredients = []
		self.directions = ''
		self.prepTime = 0
		self.cookTime = 0
		self.haveAllIngredients = False
		self.score = 0
		self.imageURL = ''

	def __str__(self):
		return self.name+'\n'+str(self.ingredients)+'\n'+str(self.score)

	def addIngredient(self, ing):
		self.ingredients.extend(ing)

	def addDirections(self, direct):
		self.directions = direct

	def addPrepTime(self, time):
		self.prepTime = time

	def addCookTime(self, time):
		self.cookTime = time

	def hasAllIngredients(self, boolean):
		self.haveAllIngredients = boolean

	def addScore(self, score):
		self.score = score

	def addImage(self, url):
		self.imageURL = url

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

def ing_on_hand(onHand,inRecipe):
	onHandList = []
	onHandList.extend(onHand)
	onHandList.extend(commonCupboard)
	onHandIngredients = [x for x in onHandList for y in inRecipe if x in y.split() if len(y) > 1]
	return onHandIngredients

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

	instruction_soup = soup.find_all("ul", {"class": "recipe-directions-list"})
	directions = ''

	for ul in instruction_soup:
		for li in ul.find_all('li'):
			directions += li.p.get_text()+"\n"

	return directions

def get_image(url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")

	imageURL = ''
	image_soup = soup.find_all("div", {"class" :"ico-wrap"})
	if not image_soup:
		image_soup = soup.find_all("a", {"class": "ico-wrap", "data-pos": "top"})
		if image_soup:
			imageURL = image_soup[0].img['src']
	else:
		imageURL = image_soup[0].img['src']

	return imageURL

# main algorithm for project
# Extracts all necessary data from the yummly api, and calls the simplicity algorithm
def evaluate_recipe(recipe):
	recipeName = recipe['name'].encode('ascii','ignore')
	print "evaluating %s" % recipeName
	
	sourceDict = recipe['source']
	sourceName = sourceDict['sourceDisplayName'].encode('ascii','ignore')
	directionsText = ""
	imageSource = ""

	# currently, only Food Network sources work. 
	if "Food Network" in sourceName:
		directionsText = get_directions(sourceDict['sourceRecipeUrl'])
		imageSource = get_image(sourceDict['sourceRecipeUrl'])
		print directionsText
		print imageSource
	else:
		return

	prepTime = 0
	if 'prepTimeInSeconds' in recipe:
		prepTime = recipe['prepTimeInSeconds']

	cookTime = 0
	if 'cookTimeInSeconds' in recipe:
		cookTime = recipe['cookTimeInSeconds']
	else:
		if prepTime == 0: # API returned non-specific cooking time
			cookTime = recipe['totalTimeInSeconds'] # will use total time as cook time in algorithm instead

	ingredientList = recipe['ingredientLines']
	numTotalIngredients = len(ingredientList)
	ingOnHand = ing_on_hand(allowedIngredients, mainIngredientRecipes[mainIngredientRecipes.index(recipe['id'])+1])
	numMissingIngr = numTotalIngredients - len(ingOnHand)

	flavors = recipe['flavors']

	if directionsText:
		rec = Recipe(recipeName)
		rec.addIngredient(mainIngredientRecipes[mainIngredientRecipes.index(recipe['id'])+1])		
		rec.addDirections(directionsText)
		rec.addPrepTime(prepTime)
		rec.addCookTime(cookTime)
		rec.hasAllIngredients(numMissingIngr == 0)

		simplicityScore = evaluate_simplicity(numTotalIngredients,prepTime,cookTime,numMissingIngr,directionsText)
		rec.addScore(simplicityScore)

		recipeList.append(rec)

# Assigns a score to a recipe based upon a number of factors 
def evaluate_simplicity(numIng, prepTime, cookTime, numMissingIngr, directionsText):
	numIngConst = 0.6
	prepConst = 0.0015
	cookConst = 0.001
	missingIngrConst = 2.0
	fkConst = 0.5
	stepsConst = 0.3

	fkScore = flesch_kincaid_score(directionsText)
	numSteps = len([s.strip() for s in directionsText.splitlines()])


	return numIngConst*numIng + prepConst*prepTime + cookConst*cookTime + missingIngrConst*numMissingIngr + fkConst*fkScore + stepsConst*numSteps

def printResults(ingList):
	print 'The simplest recipes for the ingredients ' + str(ingList) + ' are the following:'
	i = 0
	while i < len(recipeList):
		print str(i+1) + '. ' + str(recipeList[i].name) + ' - ' + str(recipeList[i].score) 
		i += 1
	
def main(argv):
	#credentials structure: _app_id=app-id&_app_key=app-key
	yummlyAppID = "1a10b2e0"
	yummlyAppKey = "72595b3dee46471a8a93caa35baf8ef1"
	yummlyCredentials = '%s=%s&%s=%s' % ('_app_id', yummlyAppID, '_app_key', yummlyAppKey)

	queryTextFile = argv[0]
	
	with open(queryTextFile) as f:
		for line in f:
			line = line.lower()
			allowedIngredients.append(line.strip())
			
	urlQuery = "q=Food+Network"
	urlIngredients = ''
	for ing in allowedIngredients:
		if ing:
			urlIngredients = urlIngredients + '&allowedIngredient[]=%s' % ing.strip()

	recipeSource = "&allowedSource=Food+Network"

	searchParamenters = urlQuery + urlIngredients + recipeSource + '&maxResult=5'
	#print searchParamenters
	
	url = 'http://api.yummly.com/v1/api/recipes?%s&%s' % (yummlyCredentials, searchParamenters)
	results = process_request(url)
	
	completeRecipes = []
	for item in results["matches"]:
		#print item['id']
		mainIngredientRecipes.append(item['id'])
		mainIngredientRecipes.append(item['ingredients'])
		completeRecipes.append(get_recipe(item['id'], yummlyCredentials))
		
	# evaluate the simplicity for every recipe gathered
	for item in completeRecipes:
		evaluate_recipe(item)
	
	recipeList.sort(key= lambda x: x.score)

	printResults(allowedIngredients)
	
	#print results
	
if __name__ == '__main__':
	main(sys.argv[1:]) # ignores passing the file named
