import json
from pprint import pprint
json_data = open('C:/Users/James/workspace/echo/out')

data = json.load(json_data)

for section in data:
	for bar in section:
	
		
		for beat in bar:
			for tantum in beat:
				pprint(tantum)


json_data.close()