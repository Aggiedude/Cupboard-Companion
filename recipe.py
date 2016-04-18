recipeList = []

class Recipe:

	def __init__(self, name):
		self.name = name
		self.ingredients = []
		self.directions = ''
		self.score = 0

	def __str__(self):
		return self.name+'\n'+str(self.ingredients)+'\n'+str(self.score)

	def addIngredient(self, ing):
		self.ingredients.extend(ing)

	def addDirections(self, direct):
		self.directions = direct

	def addScore(self, score):
		self.score = score

def addStuff(name, score, directions):
	rec = Recipe(name)
	rec.addScore(score)
	rec.addDirections(directions)
	rec.addIngredient(['eggs','milk','cheese'])

	recipeList.append(rec)

def main():
	addStuff("recipe1", 123, "Place this in the oven")
	addStuff("recipe2", 543, "Place this in the stove")
	addStuff("recipe3", 1234, "Place this in the microwave")
	addStuff("recipe4", 13, "Place this in the fridge")

	recipeList.sort(key= lambda x: x.score)

	i = 0

	while i < len(recipeList):
		print str(i+1) + '. ' + str(recipeList[i].name) + ' - ' + str(recipeList[i].score) + ' - ' + str(recipeList[i].ingredients)
		i += 1

	print recipeList[0]

if __name__ == '__main__':
	main()