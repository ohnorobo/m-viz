from pprint import pprint


chordDict = {(4,3,5):"Major", (3,4,5):"Minor", (4,4,4):"Aug", (3,3,6):"Dim", (4,6,2):"7", (7,3,2):"7", (4,7,1):"M7", (3,7,2):"m7", (3,3,3):"dim7"}
noteDict = {0:"C", 1:"C#", 2:"D", 3:"", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}

def intToNote(i):
	j = i % 12
	noteDict[i]


def properMod12(i):
	j = i % 12
	if j < 0 : 
		j = j + 12
	return j


def getChordType(w):
	v = sorted(map(lambda x: x[1], w))
	t = (v[1]-v[0] % 12, v[2]-v[1] % 12, v[0]-v[2] % 12)
	
	u = tuple(map(properMod12, t + t))
	#pprint(u)
	
	key1 = u[0:3]
	key2 = u[1:4]
	key3 = u[2:5]
	key4 = reversed(u[0:3])
	key5 = reversed(u[1:4])
	key6 = reversed(u[2:5])

	if (not ((key1 in chordDict) or (key2 in chordDict) or (key3 in chordDict) or (key4 in chordDict) or (key5 in chordDict) or (key6 in chordDict))):
		
		return "Nope!"
	elif (key1 in chordDict):
		return (w[0], chordDict[key1])
	elif (key2 in chordDict):
		return (w[1], chordDict[key2])
	elif (key3 in chordDict):
		return (w[2], chordDict[key3])
	elif (key4 in chordDict):
		return (w[2], chordDict[key4])
	elif (key5 in chordDict):
		return (w[0], chordDict[key5])
	else:
		return (w[1], chordDict[key6])




		