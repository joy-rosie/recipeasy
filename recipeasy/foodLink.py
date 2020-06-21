#! python3

import recipeasy
import inflect
import re


p = inflect.engine()

def convertToSingularAndLowerCase(word):
    # converts the noun word into singular. If singular not found, or if already singular, returns same word
    if p.singular_noun(word) == False:
        singular = word.lower()
    else:
        singular = p.singular_noun(word)
    return(singular.lower())

def getIngredient(string):
    stringWithoutBracketCont = re.sub("[\(\[].*?[\)\]]", "", string) #remove everything within brackets
    stringWithoutDigits = ''.join([i for i in stringWithoutBracketCont if not i.isdigit()]) #remove all digits in the string
    firstCommaSubstring = stringWithoutDigits.split(',')[0]
    spaceSubstrings = firstCommaSubstring.split(' ')
    powderForm = False  # initialize default value
    if len(spaceSubstrings) == 1:
         tags = [convertToSingularAndLowerCase(spaceSubstrings[0])]
    else:
        #first, gather evidence on whether the thing is in powder/liquid form. this will be important for paprika, coriander and basil which come in both powder and form and some other form
        for i in spaceSubstrings:
            if i in listOfPowderIdentifiers:
                powderForm = True
                # print(string + " HAS A POWDER MEASURE")
        tags = []
        for i in spaceSubstrings:
            if len(i) > 1: # filter out words that are one character long, as these are always not relevant
                singAndLower = convertToSingularAndLowerCase(i)
                if singAndLower not in listOfNonRelevantWords:
                    tags.append(singAndLower)
    # print(tags)
    ingredientMatchingScorecard = ''
    scores = []
    for i in range(len(databaseIngredientSubstrings)): # iterate thru every database entry

        databaseIngredientScore = 0
        for j in databaseIngredientSubstrings[i]: # iterate thru each item in the data base entry
            multiplier = 1
            if j in matchingScoreMod_x0pt3:
                multiplier = 0.3
            for k in tags:
                if j == k:
                    databaseIngredientScore = databaseIngredientScore + 1 * multiplier
            if powderForm == True and j in listOfPowderIdentifiers:
                databaseIngredientScore = databaseIngredientScore + 0.3
        databaseIngredientScore = databaseIngredientScore - len(databaseIngredientSubstrings[i])*0.1 #punish database entries for over-specifying to something that may be different to what is desired. For instance garlic vs garlic powder
        scores.append(databaseIngredientScore)
        if databaseIngredientScore > 0:
            ingredientMatchingScorecard = ingredientMatchingScorecard + databaseIngredients[i] + ': ' + str(databaseIngredientScore) + '; '
    # print(ingredientMatchingScorecard)
    if max(scores) > 0: #print the winning entry
        indexOfHighest = scores.index(max(scores))
        return(databaseIngredients[indexOfHighest])
    else:
        return('no matching ingredient found!')



listOfNonRelevantWords = ['pot','tsp','tbsp','mini','small','large','seeded','lean','bunch','handful','piece','bag','g','gram','kg','kilogram','glas','glass','frozen','and','plain','mix','mixed','cup','cups','chip','sprouting']
listOfPowderIdentifiers = ['tsp','tbsp','g','gram','ground','powdered','dried']
matchingScoreMod_x0pt3 = ['ground','dried','clove','smoked','red']

food_data = recipeasy.data.get_foods()
databaseIngredients = []
databaseIngredientSubstrings = []
for i in food_data:
    databaseIngredients.append(i)
    substrings = i.split('_')
    singularAndLowercaseSubstrings = []
    for i in substrings:
        singularAndLowercaseSubstrings.append(convertToSingularAndLowerCase(i))
    databaseIngredientSubstrings.append(singularAndLowercaseSubstrings)

txt = open(r"D:\D - Documents\Github Local Repos\Recipeasy\recipeasy\list_of_scraped_ingredients.txt", 'r')
content = txt.readlines()

scrapedIngredients = []
for i in content:
    scrapedIngredients.append(i[:-1])

for i in scrapedIngredients:
    getIngredient(i)
