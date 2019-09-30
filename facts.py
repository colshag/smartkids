'''
Fact Data
'''
import csv

myFacts = {'CULTURE':[],'ANIMALS':[],'GEOGRAPHY':[],'SPACE':[]}

# load csv scenario data
with open('facts.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for item in ['CULTURE','ANIMALS','GEOGRAPHY','SPACE']:
            try:
                if row[item] != "":
                    myFacts[item].append(row[item])
            except:
                pass

print(myFacts)