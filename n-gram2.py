import random
 
infilename = "StatusUpdate.txt"
trainingdata = open(infilename).read()
 
contextconst = [""]
 
context = contextconst
model = {}
 
for word in trainingdata.split():
    # model[key] = value. Appending to list.
    model[str(context)] = model.setdefault(str(context),[])+ [word]
    context = (context+[word])[1:]

context = contextconst
for i in range(100):
    word = random.choice(model[str(context)])
    print(word,end=" ")
    context = (context+[word])[1:]
 
print()
print()

# Calculating percentages

print("PROBABILITIES: \n\n")

for currentKey in model:
    currentValue = model[currentKey]
    print("Word: ", currentKey)
    currentPosition = 0
    usedWords = [""]

    while currentPosition < len(currentValue):

        numTimesCurrentWordHasOccured = 0
        comparisonWord = currentValue[currentPosition]
        currentPosition += 1

        if comparisonWord not in usedWords:
            for myWord in currentValue:
                if myWord == comparisonWord: # now need to skip duplicates
                    numTimesCurrentWordHasOccured += 1
            usedWords.append(comparisonWord)
            print("\t", comparisonWord, ":", (numTimesCurrentWordHasOccured / len(currentValue)) 
                * 100, "%")

# sublime setting: convert indentation to spaces! That way, Python can handle it! 