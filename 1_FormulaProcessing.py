from __future__ import division
import sys
import numpy as np, re, math

                    ####Defining functions####
#######
def returnval(list1):
     if len(list1)>0:
          return sum(list1)
     else:
          return 0.0
#######
#######
def getrat(a, b):
     '''
     Function to find ratios of elements. Avoids float division by 0. If the
     denominator is 0, this function will return the int 0.
     a and b can be floats or ints.
     Liz Mahood 12/12/17
     '''

     if b != 0 and b != 0.0:
          newval = a/b
     else:
          newval = 0

     return newval
#######

##reading in 
fafile = open(sys.argv[1], 'r')

##making output file
outfile = open(sys.argv[1] + '_augmented2.tab', 'w') 

##making headers
outfile.write('#ID\tNewFormula\tNewMIM\tnumofC\t'\
              'numofH\tnumofO\tnumofN\tnumofP\tnumofS\tHtoC\tHtoO\tCtoO\tCtoN\t'\
              'CtoS\tCtoP\tAfterdecMass\tAMD\tRMD\n')

##reading the lines
line = fafile.readline()

##some lists
mads = [] ##this contains the mass after the decimal point (Mass After Decimal)
amds = [] ##Absolute Mass Defect
rmds = [] ##Relative Mass Defect

##counter for formulas with unexpected elements
unexp = 0

##counters
x = 0; b = 0; idcounter = 1

good_els = {'C':12.000, 'H': 1.007825, 'O': 15.99491, 'N': 14.00307,
            'P': 30.97376, 'S': 31.97207}

while line:
     #More lists
     numofC = []; numofH = []; numofO = []
     numofN = []; numofP = []; numofS = []; numsof_otherels = []
     x+=1
          
     ##getting the formula
     formula = line.strip()

     ##assigning a unique instance ID to each formula
     ID = str('L' + str(idcounter))
     
     ##splitting up formula into different elements
     elnums = re.findall('[A-Z][^A-Z]*', formula)
     flag = 0

     '''
     recording the numbers of different elements
     also looks for Ds and turns into Hs, changes mim accordingly
     '''

     for element in elnums:
          brokenel = re.findall('\d+|\D+', element)
          numofD = 0
          if brokenel[0] == 'D':
               numofD = int(brokenel[1]) 
               ##adds the # of Ds in this formula to # of Hs
               numofH.append(int(numofD))
          elif brokenel[0] == 'C':
               if len(brokenel) == 2:
                    numofC.append(int(brokenel[1]))
               elif len(brokenel) == 1:
                    numofC.append(int(1))
          elif brokenel[0] == 'H':
               if len(brokenel) == 2:
                    numofH.append(int(brokenel[1]))
               elif len(brokenel) == 1:     
                    numofH.append(int(1))
          elif brokenel[0] == 'O':
               if len(brokenel) == 2:
                    numofO.append(int(brokenel[1]))
               elif len(brokenel) == 1:
                    numofO.append(int(1))
          elif brokenel[0] == 'N':
               if len(brokenel) == 2:
                    numofN.append(int(brokenel[1]))
               elif len(brokenel) == 1:
                    numofN.append(int(1))
          elif brokenel[0] == 'P':
               if len(brokenel) == 2:
                    numofP.append(int(brokenel[1]))
               elif len(brokenel) == 1:
                    numofP.append(int(1))
          elif brokenel[0] == 'S':
               if len(brokenel) == 2:
                    numofS.append(int(brokenel[1]))
               elif len(brokenel) == 1:
                    numofS.append(int(1))
          else: continue
                              
     ##making sure it adds a 0 for CHONPS elements that aren't in the
     ##particular formula
     flist = []
     
     ##Have to check that there are some CHONPS in the formula. If not: flag
     ##Ones lacking CHONPS are not written out.
     full = [numofC, numofH, numofO, numofN, numofS, numofP]
     check_list = [item for sublist in full for item in sublist]
     if sum(check_list) == 0:
          unexp += 1
          idcounter +=1
          line = fafile.readline()
          continue
          
     for thislist in full:
          nsum = sum(thislist)
          flist.append(str(nsum))
          if len(thislist) == (len(numofC) - 1):
               thislist.append(int(0))
     
     newform='C%sH%sO%sN%sS%sP%s'%(flist[0],flist[1],flist[2],
                                   flist[3],flist[4],flist[5])
     mim = sum([sum(numofC) * 12, sum(numofH) * 1.0078, sum(numofO) * 15.999,
               sum(numofN) * 14.004, sum(numofP) * 30.974, sum(numofS) * 31.972])
     mim = round(mim, 4)

     ##making ratios of the numbers of elements in each molecule
     ##First finding the numbers of elements in each molecule
               
     nh=returnval(numofH); nc=returnval(numofC); no=returnval(numofO)
     nn=returnval(numofN); ns=returnval(numofS); np=returnval(numofP)
               
                
     h2c=getrat(nh,nc); h2o= getrat(nh,no); c2o = getrat(nc,no);
     c2n = getrat(nc,nn); c2s = getrat(nc,ns); c2p = getrat(nc,np) 

               
     ##number after decimal
     mad = round(mim%1, 4)
     mads.append(mad)

     ##absolute mass defect
     roundmim = round(mim, 0)
     if round((roundmim- mim),4) >= 0:
          amd = round((roundmim - mim),4)
          amds.append(amd)
     elif round((roundmim - mim),4) < 0:
          amd = round(mad, 4)
          amds.append(amd)

     ##relative mass defect
     if mim != 0:
          rmd = int(round(((amd/mim) * 1e6),0))
          rmds.append(rmd)

     outfile.write(f'{ID}\t{newform}\t{mim}\t{nc}\t{nh}\t{no}\t{nn}\t{np}'
                   f'\t{ns}\t{h2c}\t{h2o}\t{c2o}\t{c2n}\t{c2s}\t{c2p}\t{mad}'
                   f'\t{amd}\t{rmd}\n')
     b += 1

     idcounter += 1
     line = fafile.readline()
fafile.close(); outfile.close()


print("INP lines: ", x)
print("-----")
print("Flagged: ", unexp)
print("Total lines not written to OUT: ", unexp)
print("-----")
print("OUT lines: ", b)

print("Done!")

