aarray = []
with open("domains.txt") as f:
	line = f.readlines()
	for i in line:
		i = i.split()
		for j in i:
			j = j.strip()
			try:
				int(j)
			except:
				aarray.append(j)
				pass
print(aarray)
w = open('stripped.txt','w')
for i in aarray:
	w.write(i + "\n")
