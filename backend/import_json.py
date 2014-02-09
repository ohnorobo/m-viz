import json
from chord_analysis import *
from pprint import pprint


fileBaseName = "queen"
json_data = open('C:/Users/James/workspace/echo/m-viz/templates/jsonfiles/' + fileBaseName + '.json')

def topThree(v):
	""" SPEED ME UP! Gets the biggest three elements of a vector and their indices"""
	u = sorted(zip(v,range(12)))
	
	return u[-3:]

def getMode(v):
	myDict = {}
	for e in v:
		if (e in myDict):
			myDict[e] = myDict[e] + 1
		else: myDict[e] = 1
	
	s = sorted(myDict, key=myDict.get)
	return s[-1]
	
def flatten(v):
	return [item for sublist in v for item in sublist]



data = json.load(json_data)


binaryMask = [] # corresponds to accented notes
songPitch = [0]*12
accentCount = 0
allRhythms = []

for section in data:
	sectionBinaryMask = [] # accented notes in this section
	songPitch = [a+b for a,b in (zip(songPitch, section["pitch"]))] # add all the pitches from each section
	tatumsPerSection = []
	sectionRhythm = [0]*12
	
	for bar in section["bars"]:
		tatumsPerBar = 0
		measureNotes = [] # the sum of the pitches from each accented tatum
		binaryLoudnessMask = [] # possibly accented vector by loudness
		binaryTimbreMask = [] # possibly accented vector by timbre[3]
		measureBinaryMask = [] ### Binary Mask for a measure
		
		
		for beat in bar["beats"]:
			beatBinaryMask = [] ### Binary Mask for a beak
			
			for tatum in beat["tatums"]:
				tatumsPerBar += 1
				
				if (tatum["loudness"] > bar["loudness"]): # if this tatum's loudness is greater than the bar's loudness
					l = 1
				else:
					l = 0
				binaryLoudnessMask.append(l)
				
				if (tatum["timbre"][3] > bar["timbre"][3]): # if this tatum's timbre[3] is greater than the bar's timbre[3]
															# TIMBRE[7] works better
					t = 1
				else: 
					t = 0
				binaryTimbreMask.append(t)
					
				if (tatum["timbre"][7] > bar["timbre"][7]): # if this tatum's timbre[7] is greater than the bar's timbre[7]
					r = 1
				else: 
					r = 0
					
				d = r
				beatBinaryMask.append(d)
				
				if (d == 1): # if this tatum is accented
					tatum["onBeat"] = True
					
					chord = getChordType(topThree(tatum["pitch"])) # chord is either "Nope!" or ((value noteIndex), chordType)
					if (chord == "Nope!"):
						tatum["chord"] = "None"
					else:
						tatum["chord"] = intToNote(chord[0][1]) + str(chord[1])
					
					measureNotes.append(tatum["pitch"])
					
				else:
					tatum["onBeat"] = False
					tatum["chord"] = "None"
			
			measureBinaryMask.append(beatBinaryMask)
			
			
		sectionBinaryMask.append(measureBinaryMask)	
		tatumsPerSection.append(tatumsPerBar)
		pprint("sectionRhythm")
		pprint(sectionRhythm)
		pprint("mbm")
		pprint(measureBinaryMask)
		sectionRhythm = list(map(sum, zip(sectionRhythm, flatten(measureBinaryMask))))
		
	#pprint(tatumsPerSection)
	# pprint(getMode(tatumsPerSection))
	tatumCount = getMode(tatumsPerSection)
	pprint("mode")
	pprint(tatumCount)
	pprint(sectionRhythm)
	sectionRhythm = [int(round(x / (len(section["bars"])))) for x in sectionRhythm]
	pprint(sectionRhythm)
	pprint("done rhythms")
	allRhythms.append(sectionRhythm)
	binaryMask.append(sectionBinaryMask)	
		
# pprint(songPitch)
# pprint(topThree(songPitch))
# pprint(getChordType(topThree(songPitch)))








for i in range(len(data)):
	
	for j in range(len(data[i]["bars"])):
		
		x = sum(a*b for a,b in zip(allRhythms[i], flatten(binaryMask[i][j])))
		pprint(allRhythms[i])
		pprint(flatten(binaryMask[i][j]))
		pprint(x)
		#pprint(data[i]["bars"][j])
		data[i]["bars"][j]["rhythm"] = x 

pprint(allRhythms)

		
	

f2 = open("C:/Users/James/workspace/echo/m-viz/templates/jsonfiles/newqueen.json", "w+")
data2 = json.dumps(data, indent=4)
f2.write(data2)
f2.close()

json_data.close()

#pprint(binaryMask)

