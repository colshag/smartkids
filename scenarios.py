'''
Scenario Data hardcoded for now
'''
import csv

scenarios = []
scenarioNames = []

# load csv scenario data
with open('scenarios.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        d = {}
        if 'ID' != '' and 'SCENARIO' != '':
            for item in ['SCENARIO','DIALOG']:
                d[item] = row[item]
            for item in ['ID','YES','NO','EXIT','CREW MORALE', 'SHIP STRENGTH', 'INTEL']:
                try:
                    d[item] = int(row[item])
                except:
                    d[item] = 0
            print(d)
            scenarios.append(d)

# scenarios.append({SCENARIO_NAME:'put name of scenario here',
#                   ID:0,
#                   DIALOG:'put dialog here',
#                   YES:if answer is yes goto  id indicated
#                   NO:i fanswer is no goto id indicated
#                   EXIT:'type EXIT here if this dialog then ends the scenario starting a new one',
#                   CREW_MORALE:'place a positive or negative integer if crew morale is affected by this outcome',
#                   SHIP_STRENGTH:'place a positive or negative integer if ship strength is affected by this outcome',
#                   INTEL:'place a positive or negative integer if intel is affected by this outcome'})

scenarios.append({'SCENARIO_NAME':'WELCOME MESSAGE',
                  'ID': 0,
                  'DIALOG':'You are a mixed crew of misfits on your mission to thwart a super weapon being built by a group of space pirates. As you explore keep track of your ships crew morale, and ship strength, if either goes below zero you will lose your mission. Your goal is to gather intelligence by completing scenarios on your many adventures to come. Say Yes to proceed, or Cancel to give up now.',
                  'YES':1,
                  'NO':0,
                  'EXIT':0,
                  'CREW_MORALE':0,
                  'SHIP_STRENGTH':0,
                  'INTEL':0})

scenarios.append({'SCENARIO_NAME':'DISTRESS CALL 1',
                  'ID': 1,
                  'DIALOG':'(alarm) Captain, I have picked up a distress call coming from the vega system, would you like for us to respond?',
                  'YES':3,
                  'NO':2,
                  'EXIT':0,
                  'CREW_MORALE':0,
                  'SHIP_STRENGTH':0,
                  'INTEL':0})
scenarios.append({'SCENARIO_NAME':'DISTRESS CALL 1',
                  'ID': 2,
                  'DIALOG':'Aye Aye Captain, we will avoid this beacon. Engaging warp drives (engine)',
                  'YES':0,
                  'NO':0,
                  'EXIT':1,
                  'CREW_MORALE':0,
                  'SHIP_STRENGTH':0,
                  'INTEL':0})
scenarios.append({'SCENARIO_NAME':'DISTRESS CALL 1',
                  'ID': 3,
                  'DIALOG':'(ship)Captain, we are arriving at the coordinates of the distress call. (alarm) Captain we are reading multiple distress calls from a space cruiser. Scans show multiple life forms on the ship. Shall we send a boarding crew to investigate?',
                  'YES':4,
                  'NO':2,
                  'EXIT':0,
                  'CREW_MORALE':0,
                  'SHIP_STRENGTH':0,
                  'INTEL':0})
scenarios.append({'SCENARIO_NAME':'DISTRESS CALL 1',
                  'ID': 4,
                  'DIALOG':'You beam on board the Cruiser and notice a strange acidic smell that burns your nostrils. Your crew notices multiple strange life signals from the room ahead. (engine) They have also detected a strange power surge from what looks like the engine room, this could be trouble, the hyper drive could be going critical soon. Say Yes to stay in the engine room, or Say No to go investigate the Life forms.',
                  'YES':5,
                  'NO':6,
                  'EXIT':0,
                  'CREW_MORALE':0,
                  'SHIP_STRENGTH':0,
                  'INTEL':0})
scenarios.append({'SCENARIO_NAME':'DISTRESS CALL 1',
                  'ID': 5,
                  'DIALOG':'(door) (alarm) It looks like the hyper drive is in critical condition and unstable, at most we have minutes before the drive blows. (alarm) Say yes to beam off the ship before it explodes, or say no to try and rescue the survivors before it is too late.',
                  'YES':8,
                  'NO':6,
                  'EXIT':'',
                  'CREW_MORALE':'',
                  'SHIP_STRENGTH':'',
                  'INTEL':''})
scenarios.append({'SCENARIO_NAME':'DISTRESS CALL 1',
                  'ID': 6,
                  'DIALOG':'(door) You manage to access the room and your crew discovers a handful of aliens tending to their wounded. The crew detects a dangerous increase in hyperdrive levels from the engine room, (engine) (alarm) we need to beam off this ship! Do you bring the wounded aliens with your crew?',
                  'YES':7,
                  'NO':8,
                  'EXIT':0,
                  'CREW_MORALE':0,
                  'SHIP_STRENGTH':0,
                  'INTEL':0})
scenarios.append({'SCENARIO_NAME':'DISTRESS CALL 1',
                  'ID': 7,
                  'DIALOG':'(large_explosion) The Cruiser explodes at a safe distance and after some time your crew manages to piece together what happened, it is a good thing we saved the aliens, we learned some information about the pirate fleet. You have gained 10 intelligence and 5 crew morale.',
                  'YES':0,
                  'NO':0,
                  'EXIT':1,
                  'CREW_MORALE':5,
                  'SHIP_STRENGTH':0,
                  'INTEL':10})
scenarios.append({'SCENARIO_NAME':'DISTRESS CALL 1',
                  'ID': 8,
                  'DIALOG':'(large_explosion) The Cruiser explodes at a safe distance and after some time your crew manages to gather some interesting technology which will help increase your ships strength, however, the crew is not happy that we abandoned a crew in need. You lost 10 crew morale and gained 10 ship strength.',
                  'YES':0,
                  'NO':0,
                  'EXIT':1,
                  'CREW_MORALE':-10,
                  'SHIP_STRENGTH':10,
                  'INTEL':0})