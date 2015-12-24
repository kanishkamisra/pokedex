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

# Clean!
def brackets(word):
	list = [x for x in word]
	for i in range(1, len(list)):
		if list[i].isupper():
			list[i] = ' ' + list[i]
	new_list = ''.join(list).split(' ')
	if len(new_list) > 1:
		new_list.insert(1,'(')
		new_list.append(')')
	return ' '.join(new_list)

def breaks(word):
	list = [x for x in word]
	for i in range(1, len(list)):
		if list[i].isupper():
			list[i] = ' ' + list[i]
	new_list = ''.join(list).split(' ')
	return new_list

for data in data_list:
	data['Name'] = brackets(data['Name'])
 	data['Type'] = breaks(data['Type'])

# Dump to json
with open('pokemondata.json', 'wb') as jsonfile:
	json.dump(data_list, jsonfile)
	print 'Data saved to json!'


