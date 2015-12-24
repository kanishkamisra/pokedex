import requests
import lxml.html as lh
import json

url = 'http://pokemondb.net/pokedex/all'
page = requests.get(url)
doc = lh.fromstring(page.content)

#Store data from the table into a list
elements = doc.xpath('//tr')

col = []
i=0

# Store headers as tuples with each header being associated with a list
for e in elements[0]:
	i+=1
	name = e.text_content()
	col.append((name,[]))

# Let's populate!
for j in range(1,len(elements)):
	E = elements[j]

	if len(E) != 10:
		break

	i=0
	for e in E.iterchildren():
		data = e.text_content()
		if i>0:
			try:
				data = int(data)
			except:
				pass
		col[i][1].append(data)
		i+=1

data_list = []
# Populate a separate list with json formatted data.
for i in range(0,len(elements)-1):
	data_list.append({column: entry[i] for (column, entry) in col})

# Dump to json
with open('pokemondata.json', 'wb') as jsonfile:
	json.dump(data_list, jsonfile)


