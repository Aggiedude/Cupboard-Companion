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

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/about-us")
def aboutUs():
	return render_template('about-us.html')
	
@app.route("/recipe-list", methods=['POST'])
def recipeList():

	form = request.form

	keys = form.keys()
	allowedIngredients = []
	disallowedIngredients = []
	courseTypes = []

	for key in keys:
		if key[:3] == 'ing':
			allowedIngredients.append(form[key].encode('ascii','ignore'))
		elif key[:3] == 'xin':
			disallowedIngredients.append(form[key].encode('ascii','ignore'))
		else:
			courseTypes.append(key.encode('ascii','ignore'))

	begin_recipe_searching(allowedIngredients, disallowedIngredients, courseTypes)

	return render_template('recipe-list.html', list=tempList)

@app.route("/recipe-list/view")
def viewRecipeList():
	# global tempList
	# tempList = []

	# rec1 = Recipe('Recipe 1')
	# rec1.addIngredient(['cheese', 'eggs'])
	# rec1.addMeasuredIngredient(['2/3 cup cheese', ' 3 eggs'])
	# rec1.addScore(12)
	# rec1.addDirections("Place this in the oven")
	# rec1.addPrepTime('1 hr')
	# rec1.addTotalTime('1 hr')
	# rec1.hasAllIngredients(True)
	# rec1.addImage('http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2003/10/16/3/tm1b51_grilled_cheese.jpg.rend.sni12col.landscape.jpeg')

	# rec2 = Recipe('Recipe 2')
	# rec2.addIngredient(['cheese','eggs', 'milk','bread'])
	# rec2.addMeasuredIngredient(['1/2 cup cheese','2 eggs', '1 cup milk'])
	# rec2.addScore(50)
	# rec2.addDirections("Place this in the mirowave")
	# rec2.addCookTime('50 min')
	# rec2.addPrepTime('20 min')
	# rec2.addTotalTime('1 hr 10 min')
	# rec2.addImage('http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2010/3/25/0/FNM_050110-Cover-002_s4x3.jpg.rend.sni12col.landscape.jpeg')

	# rec3 = Recipe('Recipe 3')
	# rec3.addIngredient(['bread'])
	# rec3.addMeasuredIngredient(['3 loaves bread'])
	# rec3.addScore(6)
	# rec3.addDirections("Place this in the stove")
	# rec3.addCookTime('1 hr 10 min')
	# rec3.addTotalTime('1 hr 10 min')
	# rec3.addImage('http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2008/7/2/0/PB0108_Chicken-Salad-Sliders.jpg.rend.sni12col.landscape.jpeg')

	# rec4 = Recipe('Recipe 4')
	# rec4.addIngredient(['cheese','eggs', 'bread', 'onion', 'garlic', 'pepper'])
	# rec4.addMeasuredIngredient(['1 cup cheese','2 scrambled eggs', '2 slices bread', '1 diced onion'])
	# rec4.addScore(78)
	# rec4.addDirections("Place this in the fridge")
	# rec4.addCookTime('20 min')
	# rec4.addPrepTime('10 min')
	# rec4.addTotalTime('30 min')
	# rec4.addImage('http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2007/3/8/0/tu0211_sandwich.jpg.rend.sni12col.landscape.jpeg')

	# tempList.append(rec1)
	# tempList.append(rec2)
	# tempList.append(rec3)
	# tempList.append(rec4)

	# tempList.sort(key= lambda x: x.score)
	# return render_template('recipe-list.html', list = tempList)
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
	# while i < len(tempList):
	# 	if tempList[i].name == str(recName):
	# 		recIndex = i
	# 		break
	# 	i+=1

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

	direction_soup = soup.find_all(itemprop='recipeInstructions')[0].p
	directions = direction_soup.get_text() + "\n"
	siblings = direction_soup.find_next_siblings("p")
	siblings = siblings[:-2]

	for sibling in siblings:
		directions += sibling.get_text() + "\n"

	return directions

# Scrapes the source HTML page gathered from the yummly api for recipe image 
# currently only works with recipes taken from foodnetwork.com
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
def evaluate_recipe(allowedIngredients, recipe):
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
		rec.addDirections(directionsText)
		rec.addImage(imageSource)
		rec.addPrepTime(prepTimeProper)
		rec.addCookTime(cookTimeProper)
		rec.addTotalTime(totalTimeProper)
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
	
def begin_recipe_searching(allowedIngredients, disallowedIngredients, courseTypes):
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
			urlIngredients = urlIngredients + '&allowedIngredient[]=%s' % ing.strip()
	for ing in disallowedIngredients:
		if ing:
			urlXIngredients = urlXIngredients + '&excludedIngredient[]=%s' % ing.strip()
	for course in courseTypes:
		if course:
			urlCourseTypes = urlCourseTypes + '&allowedCourse[]=course^course-%s' % ing.strip()

	recipeSource = "&allowedSource=Food+Network"

	searchParamenters = urlQuery + urlIngredients + recipeSource + '&maxResult=10'
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
		evaluate_recipe(allowedIngredients, item)
	
	recipeList.sort(key= lambda x: x.score)

	printResults(allowedIngredients)
	
	#print results

if __name__ == "__main__":
	app.run()