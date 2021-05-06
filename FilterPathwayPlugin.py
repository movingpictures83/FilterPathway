import sys
#import numpy
#from plugins.CSV2GML.CSV2GMLPlugin import *
from CSV2GML.CSV2GMLPlugin import *
import PyPluMA


class FilterPathwayPlugin(CSV2GMLPlugin):
   def input(self, filename):
      # Format expected:
      # correlationfile <somefile.csv>
      # pathwayfile <somefile.txt>
      thefile = open(filename, 'r')
      for line in thefile:
         myline = line.strip()
         entries = myline.split('\t')
         if (entries[0] == 'correlationfile'):
            self.myfile = PyPluMA.prefix()+"/"+entries[1]
         elif (entries[0] == 'pathwayfile'):
            self.mypathways = PyPluMA.prefix()+"/"+entries[1]
         # Ignore everything else

   def run(self):
      # Read CSV file
      filestuff = open(self.myfile, 'r')
      self.firstline = filestuff.readline().strip()
      self.bacteria = self.firstline.split(',')
      if (self.bacteria.count('\"\"') != 0):
         self.bacteria.remove('\"\"')
      self.n = len(self.bacteria)
      self.ADJ = []
      i = 0
      for line in filestuff:
         contents = line.split(',')
         self.ADJ.append([])
         for j in range(self.n):
            value = float(contents[j+1])
            self.ADJ[i].append(value)
         i += 1
      # Read Pathways file
      self.keeplines = []
      pathwaystuff = open(self.mypathways, 'r')
      for line in pathwaystuff:
         myline = line.strip()
         myline = myline[myline.find('INVOLVES:')+9:]
         elements = myline.split('\t')
         while (elements.count('') != 0):
            elements.remove('')
         bioelements = []
         for item in elements:
            for j in range(len(self.bacteria)):
               if (item[0] == 'X' and item[1].isdigit()):
                  if (self.bacteria[j] == item or 
                      self.bacteria[j] == '"'+item+'"'): #Exactly matching metabolite
                     bioelements.append(j)
               elif (self.bacteria[j].find(item) != -1): #Containing bateria name
                  bioelements.append(j)
                  #print "FOUND BACTERIA: ", item, " AND ", self.bacteria[j]
       
         # Look for at least one edge with two bioelements
         keep = []
         for j in range(len(bioelements)):
            keep.append(False)
         flag = False
         for j in range(len(bioelements)):
            for k in range(j+1, len(bioelements)):
               if (self.ADJ[bioelements[j]][bioelements[k]] != 0):
                    keep[j] = True
                    keep[k] = True
                    flag = True
         if (flag):
            myline2 = line.strip()
            linetokeep = myline2[:myline2.find('INVOLVES:')+9]
            for j in range(len(bioelements)):
               if keep[j]:
                  linetokeep += '\t' + self.bacteria[bioelements[j]]
            linetokeep += '\n'
            self.keeplines.append(linetokeep)
         #for j in range(len(bioelements)):
         #   for k in range(len(bioelements)):
         #      self.ADJ2[bioelements[j]][bioelements[k]] = 1

      #for i in range(self.n):
      #   for j in range(self.n):
      #      self.ADJ[i][j] *= self.ADJ2[i][j]


   def output(self, filename):
      filestuff2 = open(filename, 'w')
      for line in self.keeplines:
         filestuff2.write(line)
      #filestuff2.write(self.firstline+"\n")

      #for i in range(self.n):
      #   filestuff2.write(self.bacteria[i]+',')
      #   for j in range(self.n):
      #      filestuff2.write(str(self.ADJ[i][j]))
      #      if (j < self.n-1):
      #         filestuff2.write(",")
      #      else:
      #         filestuff2.write("\n")



