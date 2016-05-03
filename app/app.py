import urllib2, json, string, base64, re, sys, time
from bs4 import BeautifulSoup
from textstat.textstat import textstat
from flask import Flask, render_template, request, json, url_for

recipeList = []
mainIngredientRecipes = []
tempList = []
commonCupboard = ['salt','egg','eggs','butter','oil','sugar','granulated sugar','pepper','garlic','milk','all-purpose flour','flour','water']
madeSearch = False

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')

class Recipe:

	def __init__(self, name):
		self.name = name
		self.ingredients = []
		self.measuredIngredients = []
		self.shownIngredients = []
		self.directions = ''
		self.prepTime = ''
		self.cookTime = ''
		self.totalTime = ''
		self.haveAllIngredients = False
		self.score = 0
		self.imageURL = ''
		self.sourceURL = ''

	def __str__(self):
		return self.name+'\n'+str(self.ingredients)+'\n'+str(self.score)

	def addIngredient(self, ing):
		self.ingredients.extend(ing)
		if(len(ing) > 4) :
			self.shownIngredients = ing[:4]
			self.shownIngredients.append("...")
		else :
			self.shownIngredients.extend(ing)

	def addMeasuredIngredient(self, measuredIng):
		self.measuredIngredients.extend(measuredIng)

	def addDirections(self, direct):
		self.directions = direct

	def addTotalTime(self, time):
		self.totalTime = time

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

	def addSourceURL(self, url):
		self.sourceURL = url

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/about-us")
def aboutUs():
	return render_template('about-us.html')
	
@app.route("/recipe-list/<rush>", methods=['POST'])
def recipeList(rush):

	form = request.form

	keys = form.keys()
	allowedIngredients = []
	disallowedIngredients = []
	courseTypes = []
	inRush = False

	for key in keys:
		if key[:3] == 'ing':
			allowedIngredients.append(form[key].encode('ascii','ignore'))
		elif key[:3] == 'xin':
			disallowedIngredients.append(form[key].encode('ascii','ignore'))
		else:
			courseTypes.append(key.encode('ascii','ignore'))

	if int(rush) is 1:
		inRush = True
		print inRush
	print inRush

	begin_recipe_searching(allowedIngredients, disallowedIngredients, courseTypes, inRush)

	return render_template('recipe-list.html', list=tempList)

@app.route("/recipe-list/view")
def viewRecipeList():
	global recipeList

	try:
		if len(recipeList) == 0:
			return render_template('error.html', search=madeSearch)
	except:
		return render_template('error.html', search=madeSearch)

	return render_template('recipe-list.html', list = recipeList)

@app.route('/recipe/<recName>')
def viewRecipe(recName):
	print "got here"
	recIndex = None
	i = 0

	# return render_template('recipe.html', recipe=tempList[recIndex])
	while i < len(recipeList):
		if recipeList[i].name == str(recName):
			recIndex = i
			break
		i+=1
	
	return render_template('recipe.html', recipe=recipeList[recIndex])

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
	value = 0
	try:
		value = (0.39*(wordCount/sentenceCount)+11.8*(sylCount/wordCount) - 15.59)
	except:
		value = 0

	return value

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
def get_directions(source, url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")
	directions = ''

	if "foodnetwork" in source:
		direction_soup = soup.find_all("ul", {"class" : "recipe-directions-list"})
		for ul in direction_soup:
			for li in ul.find_all('li'):
				if "copyright" not in li.get_text().lower():
					if "courtesy" not in li.get_text().lower():
						directions += li.get_text() + '\n'
			
	elif "allrecipes" in source:
		instruction_soup = soup.find_all("ol", {"class": "list-numbers recipe-directions__list"})
		for ol in instruction_soup:
			for li in ol.find_all('li'):
				directions += li.find("span", {"class": "recipe-directions__list--item"}).get_text() + '\n'

	elif "food.com" in source:
		print "food.com directions scrape"
		direction_soup = soup.find_all("div", {"class" : "directions"})
		for li in direction_soup[0].find_all("ol"):
			directions += li.get_text() + '\n'

	return directions

# Scrapes the source HTML page gathered from the yummly api for recipe image 
# currently only works with recipes taken from foodnetwork.com
def get_image(source, url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "html.parser")

	imageURL = ''
	try:
		if 'foodnetwork' in source:
			print 'scraping image for foodnetwork'
			image_soup = soup.find_all("div", {"class" :"ico-wrap"})
			if not image_soup:
				image_soup = soup.find_all("a", {"class": "ico-wrap", "data-pos": "top"})
				if image_soup:
					imageURL = image_soup[0].img['src']
			else:
				imageURL = image_soup[0].img['src']

		elif 'food.com' in source:
			print 'scraping image for food.com'
			image_soup = soup.find_all("div", {"class" : "trans-img"})
			if not image_soup:
				print 'NO ERROR - No image'
				imageURL = ""
			else:
				imageURL = image_soup[0].img['data-src']

		print imageURL

	except:
		print 'ERROR - No image'
		imageURL = ''

	return imageURL

# main algorithm for project
# Extracts all necessary data from the yummly api, and calls the simplicity algorithm
def evaluate_recipe(allowedIngredients, recipe):
	recipeName = recipe['name'].encode('ascii','ignore')
	print "evaluating %s" % recipeName
	
	sourceDict = recipe['source']
	sourceName = sourceDict['sourceDisplayName'].encode('ascii','ignore')
	directionsText = ""
	imageSource = ""
	sourceURL = sourceDict['sourceRecipeUrl']
	print "SOURCE is: " + sourceURL

	# currently, only Food Network sources work. 
	if "Food Network" in sourceName:
		directionsText = get_directions('foodnetwork', sourceURL)
		imageSource = get_image('foodnetwork', sourceURL)
		print directionsText
		print imageSource
	elif "Food.com" in sourceName:
		print "source name is food.com"
		directionsText = get_directions('food.com', sourceURL)
		imageSource = get_image('food.com', sourceURL)
		print directionsText
		print imageSource
	elif "AllRecipes" in sourceName:
		directionsText = get_directions("allrecipes", sourceURL)
		imageSource = recipe['images'][0]['imageUrlsBySize']['360']
		print directionsText
		print imageSource
	else:
		return

	totalTimeProper = recipe['totalTime']
	prepTime = 0
	prepTimeProper = ''
	if 'prepTimeInSeconds' in recipe:
		prepTime = recipe['prepTimeInSeconds']
		prepTimeProper = recipe['prepTime']

	cookTime = 0
	cookTimeProper = ''
	if 'cookTimeInSeconds' in recipe:
		cookTime = recipe['cookTimeInSeconds']
		cookTimeProper = recipe['cookTime']
	else:
		if prepTime == 0: # API returned non-specific cooking time
			cookTime = recipe['totalTimeInSeconds'] # will use total time as cook time in algorithm instead
			cookTimeProper = recipe['totalTime']

	ingredientList = recipe['ingredientLines']
	numTotalIngredients = len(ingredientList)
	ingOnHand = ing_on_hand(allowedIngredients, mainIngredientRecipes[mainIngredientRecipes.index(recipe['id'])+1])
	numMissingIngr = numTotalIngredients - len(ingOnHand)

	flavors = recipe['flavors']

	if directionsText:
		rec = Recipe(recipeName)
		rec.addIngredient(mainIngredientRecipes[mainIngredientRecipes.index(recipe['id'])+1])
		rec.addMeasuredIngredient(ingredientList)		
		rec.addDirections([s.strip().encode('ascii', 'ignore') for s in directionsText.splitlines()])
		rec.addImage(imageSource)
		rec.addPrepTime(prepTimeProper)
		rec.addCookTime(cookTimeProper)
		rec.addTotalTime(totalTimeProper)
		rec.hasAllIngredients(numMissingIngr == 0)
		rec.addSourceURL(sourceURL)

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
	stepsConst = 0.2

	fkScore = flesch_kincaid_score(directionsText)
	numSteps = len([s.strip() for s in directionsText.splitlines()])


	return numIngConst*numIng + prepConst*prepTime + cookConst*cookTime + missingIngrConst*numMissingIngr + fkConst*fkScore + stepsConst*numSteps

def printResults(ingList):
	print 'The simplest recipes for the ingredients ' + str(ingList) + ' are the following:'
	i = 0
	while i < len(recipeList):
		print str(i+1) + '. ' + str(recipeList[i].name) + ' - ' + str(recipeList[i].score) 
		i += 1
	
def begin_recipe_searching(allowedIngredients, disallowedIngredients, courseTypes, inRush):
	#credentials structure: _app_id=app-id&_app_key=app-key
	global recipeList
	global madeSearch
	recipeList = []
	madeSearch = True

	yummlyAppID = "1a10b2e0"
	yummlyAppKey = "72595b3dee46471a8a93caa35baf8ef1"
	yummlyCredentials = '%s=%s&%s=%s' % ('_app_id', yummlyAppID, '_app_key', yummlyAppKey)
			
	urlQuery = "q=Food+Network"
	urlIngredients = ''
	urlXIngredients = ''
	urlCourseTypes = ''
	for ing in allowedIngredients:
		if ing:
			ing = string.replace(ing, " ", "%20")
			urlIngredients = urlIngredients + '&allowedIngredient[]=%s' % ing.strip()
	for xing in disallowedIngredients:
		if xing:
			xing = string.replace(xing, " ", "%20")
			urlXIngredients = urlXIngredients + '&excludedIngredient[]=%s' % xing.strip()
	for course in courseTypes:
		if course:
			urlCourseTypes = urlCourseTypes + '&allowedCourse[]=course^course-%s' % ing.strip()

	print str(urlIngredients)
	print str(urlXIngredients)

	completeRecipes = []

	# Food Network Call
	print "Calling Food Network"
	searchParamenters = urlQuery + urlIngredients + urlXIngredients + urlCourseTypes + '&maxResult=4'
	
	if inRush:
		searchParamenters += '&maxTotalTimeInSeconds=2100'
	
	url = 'http://api.yummly.com/v1/api/recipes?%s&%s' % (yummlyCredentials, searchParamenters)
	results = process_request(url)

	for item in results["matches"]:
		#print item['id']
		mainIngredientRecipes.append(item['id'])
		mainIngredientRecipes.append(item['ingredients'])
		completeRecipes.append(get_recipe(item['id'], yummlyCredentials))

	# AllRecipes Call
	print "Calling AllRecipes"
	urlQuery = "q=allrecipes"
	searchParamenters = urlQuery + urlIngredients + urlXIngredients + urlCourseTypes + '&maxResult=4'
	if inRush:
		searchParamenters += '&maxTotalTimeInSeconds=2100'
	
	url = 'http://api.yummly.com/v1/api/recipes?%s&%s' % (yummlyCredentials, searchParamenters)
	results = process_request(url)
	
	for item in results["matches"]:
		mainIngredientRecipes.append(item['id'])
		mainIngredientRecipes.append(item['ingredients'])
		completeRecipes.append(get_recipe(item['id'], yummlyCredentials))

	# Food.com Call
	print "Calling Food.com"
	urlQuery = "q=foodcom"
	searchParamenters = urlQuery + urlIngredients + urlXIngredients + urlCourseTypes + '&maxResult=4'
	if inRush:
		searchParamenters += '&maxTotalTimeInSeconds=2100'
	
	url = 'http://api.yummly.com/v1/api/recipes?%s&%s' % (yummlyCredentials, searchParamenters)
	results = process_request(url)
	
	for item in results["matches"]:
		mainIngredientRecipes.append(item['id'])
		mainIngredientRecipes.append(item['ingredients'])
		completeRecipes.append(get_recipe(item['id'], yummlyCredentials))


	# evaluate the simplicity for every recipe gathered
	for item in completeRecipes:
		evaluate_recipe(allowedIngredients, item)
	
	recipeList.sort(key= lambda x: x.score)

	printResults(allowedIngredients)
	
	#print results

if __name__ == "__main__":
	app.run()