import statistics

print("Write a function that reads a CSV file with two columns: Name and Score")
print("Return the average score, and print all names whose score is above average.")
print("")

fileInput = open("exercise-1-input.csv")

# skip the first line, which has column-headers
next(fileInput)

allScores = []
allNames = []

for line in fileInput:
    lineSplitUp = line.split(",")
    allNames.append(lineSplitUp[0])
    allScores.append(int(lineSplitUp[1]))

averageScore = round(statistics.fmean(allScores), 2)
print("The average test score is: ", averageScore)

print("The students with an above average score are:")
for i in range(len(allNames)):
    if (allScores[i] > averageScore):
        print(allNames[i], "with", allScores[i])
