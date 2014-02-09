import json
from chord_analysis import *
from pprint import pprint


fileBaseName = "circle_of_life"
json_data = open('C:/Users/James/workspace/echo/m-viz/frontend/templates/jsonfiles/' + fileBaseName + '.json')

def topThree(v):
	""" SPEED ME UP! Gets the biggest three elements of a vector and their indices"""
	u = sorted(zip(v,range(12)))
	
	return u[-3:]
	



data = json.load(json_data)

binaryMask = []
songPitch = [0]*12
accentedNotes = []


for section in data:
	sectionBinaryMask = []
	
	##pprint(songPitch)
	##pprint(section["pitch"])
	pprint("YO")
	songPitch = [a+b for a,b in (zip(songPitch, section["pitch"]))]
	
	
	for bar in section["bars"]:
		measureNotes = []
		##pprint(topThree(bar["pitch"]))	
		##pprint(getChordType(topThree(bar["pitch"])))
		pprint(bar["start_time"])
		
		binaryLoudnessMask = []
		binaryTimbreMask = []
		measureBinaryMask = [] ### Binary Mask for a measure
		
		
		for beat in bar["beats"]:
			beatNotes = []
			beatBinaryMask = [] ### Binary Mask for a beak
			
			for tatum in beat["tatums"]:
				if (tatum["loudness"] > bar["loudness"]):
					l = 1
				else:
					l = 0
				binaryLoudnessMask.append(l)
				
				if (tatum["timbre"][3] > bar["timbre"][3]):
					t = 1
				else: 
					t = 0
				binaryTimbreMask.append(t)
					
				if (tatum["timbre"][7] > bar["timbre"][7]):
					r = 1
				else: 
					r = 0
					
				d = r# max(l, t)
				beatBinaryMask.append(d)
				
				if (d == 1): 
					tatum["onBeat"] = True
					
					chord = getChordType(topThree(tatum["pitch"]))
					if (chord == "Nope!"):
						tatum["chord"] = "None"
					else:
						tatum["chord"] = intToNote(chord[0][1]) + str(chord[1])
					
					measureNotes.append(tatum["pitch"])
					# pprint("")
					# pprint(topThree(tatum["pitch"]))
					# pprint(getChordType(topThree(tatum["pitch"])))
					# pprint("")
					# 1
				else:
					tatum["onBeat"] = False
					tatum["chord"] = "None"
			
			measureBinaryMask.append(beatBinaryMask)
			#measureNotes.append(beatNotes)
			
		sectionBinaryMask.append(measureBinaryMask)	
		##pprint("measureNotes")
		##pprint(measureNotes)
		b = [0]*12
		
		for a in measureNotes:
			b = map(sum, zip(a, b))
			#pprint(a)
		
		pprint(getChordType(topThree(list(b))))
		
	binaryMask.append(sectionBinaryMask)	
		
		#measureBinaryMask = [a*b for a,b in zip(binaryLoudnessMask,binaryTimbreMask)] 
		#pprint(binaryLoudnessMask)
		#pprint(binaryTimbreMask)
		#pprint(measureBinaryMask)
		#pprint("")
	
	


		
		
#pprint(binaryMask)
#pprint(getChordType(((.1, 6), (.2, 0), (.4,2))))
pprint(songPitch)
pprint(topThree(songPitch))
pprint(getChordType(topThree(songPitch)))

f2 = open("C:/Users/James/workspace/echo/m-viz/frontend/templates/jsonfiles/newqueen.json", "w+")
data2 = json.dumps(data, indent=4)
f2.write(data2)
f2.close()


### Write song information out to a file for playback

f = open(fileBaseName + ".schd", "w")

for i in range(len(data)):
	f.write("type=s" + str(i) + "Start time=" + str(data[i]["start_time"]) + "\n")
	
	for j in range(len(data[i]["bars"])):
			
		for k in range(len(data[i]["bars"][j]["beats"])):
			
			############################################################################################
			### Tatums
			for n in range(len(data[i]["bars"][j]["beats"][k]["tatums"])):
				t = data[i]["bars"][j]["beats"][k]["tatums"][n]
				f.write("type=t" + str(n) + "b" + str(k) + "m" + str(j) + "s" + str(i) + "Start time=" + str(t["start_time"]))
				
				if(binaryMask[i][j][k][n] == 1):
					isOnBeat = True
				else:
					isOnBeat = False
				
				f.write("on_beat=" + str(isOnBeat))
				
				
				if(isOnBeat):
					t3 = topThree(t["pitch"])
					f.write("t3=" + str(t3[1]))
					
					chord = getChordType(t3)
					# pprint("chord")
					# pprint(str(chord))
					# pprint(str(chord[1]))
					# pprint(str(chord[0]))
					# pprint(str(chord[0][0]))
					# pprint(str(chord[0][1]))
					
					if(chord == "Nope!"):
						f.write("chord=None")
					else:
						f.write("chord=" + str(intToNote(chord[0][1])) + str(chord[1]))

					f.write("\n")
				### Tatum information above
			############################################################################################
			### Beat information below
			b = data[i]["bars"][j]["beats"][k]
			f.write("type=b" + str(k) + "m" + str(j) + "s" + str(i) + "Start time=" + str(b["start_time"]) + "\n")
			
			
			### Beat information above
		############################################################################################
		### Measure information below
		m = data[i]["bars"][j]
		f.write("type=m" + str(j) + "s" + str(i) + "Start time=" + str(m["start_time"]) + "\n")
		
		
		
		
		
		
		### Measure information above
	############################################################################################
	### Section information below
	
	
	### Section information above
############################################################################################



f.close()

json_data.close()

pprint(binaryMask)

