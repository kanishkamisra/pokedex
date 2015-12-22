import requests
import lxml.html as lh

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
	# print '%d: %s' % (i,name)
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

# print [len(E) for (title,E) in col]

data_dict = { column:entry for (column, entry) in col }

