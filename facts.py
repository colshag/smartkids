'''
Fact Data
'''
import csv

myFacts = {'CULTURE':[],'ANIMALS':[],'GEOGRAPHY':[],'SPACE':[]}

# load csv scenario data
with open('facts.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            if row['CATEGORY'] in myFacts.keys():
                row['ID'] = len(myFacts[row['CATEGORY']])
                myFacts[row['CATEGORY']].append(row)
        except:
            pass

print(myFacts)
