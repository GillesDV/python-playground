import statistics
import csv

print("Write a function that reads a CSV file with two columns: Name and Score")
print("Return the average score, and print all names whose score is above average.")
print("")

allRecords = []

with open("exercise-1-input.csv") as f:
    reader = csv.reader(f)
    next(reader)  # skip the first line, which has column-headers

    for name, score in reader:
        allRecords.append((name, int(score)))

# loop over each tuple in allRecords, and unpacks it into two variables.
# _ is the name (which we don't care about right now), s is the score
scores = [s for _, s in allRecords]
averageScore = round(statistics.fmean(scores), 2)

print("The average test score is: ", averageScore)
print("Students with above-average scores:")

for name, score in allRecords:
    if score > averageScore:
        print(name, "with", score)
