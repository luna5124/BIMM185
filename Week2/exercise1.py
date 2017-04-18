import os

mylist = []
for file in os.listdir("."):
	if os.path.isdir(file):
		report = os.path.join(file+"/"+file + "/" + "report.tbl")
		with open(report,'r') as input:
			score = input.readlines()[2].split('\t')[3]
			mylist.append((file,score))	
			#print file,'\t',score		
		#print(os.path.join(file+"/"+file + "/" + "report.tbl"))
mylist.sort(key=lambda x:x[1],reverse=True)

for line in mylist:
	print(line[0]+"\t"+line[1])

#print(mylist)
