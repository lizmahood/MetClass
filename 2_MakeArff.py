import sys
##INP1: eratios file
##INP2: Names of possible classes, with commas separating each class. No spaces

##reading in the input data file
file1=open(sys.argv[1],'r').readlines()

##getting the class names
inclasses = str(sys.argv[2].strip())

##opening the file, reading lines
file1=open(sys.argv[1],'r')
line1=file1.readline()

##making list of attributes
ilist=range(1,18)
newilist = list(range(2,18)) ##must exclude molecular formula
newilist.insert(0,0)
#newilist.insert(0,0)
plist=['numeric']*17
nlist=[]; vlist=[]; datalist = []

##Extracting data from input file
while line1:
    
    ##Getting attribute names, they are the column names of the input file
    if line1.startswith('#ID'):
        tab1=line1.strip().split('\t')
        for i in ilist:
            ##these are the names of attributes, putting them in nlist
            nlist.append(tab1[i])

    ##adding data to other lists
    else:
        tab1=line1.strip().split('\t')

        #Add all molecules' values to an ordered list
        vlist=[]

        for i in newilist:
            vlist.append(tab1[i])

        ##this is a list of lists, one list of attribute values per molecule
        datalist.append(vlist)

    line1=file1.readline()
file1.close()

##Writing out in arff format
out1=open(sys.argv[1]+".challenge.multi.arff",'w')
out1.write('@relation\tTestCompoundsClassifiedIntoLipidMAPSCategories\n\n')

##First writing out attribute names
out1.write('@attribute\tID\tstring\n')
for i in range(1,len(nlist)): 
    item=nlist[i]
    prop=plist[int(i-1)]
    out1.write(f'@attribute\t{item}\t{prop}\n')
    
##now writing out all possible class names
out1.write(f'@attribute\tclass\t{{{inclasses}}}\n')

##and now data
out1.write('\n@data\n')

for line in datalist:
    ##writing out attribute values for each instance
    vline = ','.join(map(str, line))
    out1.write(f'{vline},?\n')

out1.close()
print("Done!")