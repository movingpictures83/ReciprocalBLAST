#reciprocal blast- blast two files against one another
#takes input as blast outputs 
#python reciprocal blast.py blastoutput1 blastoutput2 result
Usage = """RBH BLASTOUTPUT1 BLASTOUTPUT2 RBH-list-outfile """

import sys, re
import PyPluMA
#if len(sys.argv) < 3:
#        print(Usage)


class ReciprocalBLASTPlugin:
   def input(self, infile):
                inputfile = open(infile, 'r')
                self.parameters = dict()
                for line in inputfile:
                   contents = line.strip().split('\t')
                   self.parameters[contents[0]] = contents[1]
                self.infl1 = PyPluMA.prefix() + "/" + self.parameters["infile1"]
                self.infl2 = PyPluMA.prefix() + "/" + self.parameters["infile2"]

   def run(self):
      debug = 9

      #parse first BLAST results
      FL1 = open(self.infl1, 'r')
      D1 = {} #dictionary for BLAST file ONE
      for Line in FL1:
              if ( Line[0] != '#' ):
                      Line.strip()
                      Elements = re.split('\t', Line)
                      queryId = Elements[0]
                      subjectId = Elements[1]
                      if ( not ( queryId in D1.keys() ) ):
                              D1[queryId] = subjectId  #pick the first hit
      
      if (debug): D1.keys() 
      
      #parse second BLAST results
      FL2 = open(self.infl2, 'r')
      D2 = {}
      for Line in FL2:
              if ( Line[0] != '#' ):
                      Line.strip()
                      Elements = re.split('\t', Line)
                      queryId = Elements[0]
                      subjectId = Elements[1]
                      if ( not ( queryId in D2.keys() ) ):
                              D2[queryId] = subjectId  #pick the first hit
      
      if (debug): D2.keys() 
      
      #Now, pick the share pairs
      
      self.SharedPairs={}
      for id1 in D1.keys():
              value1 = D1[id1]
              if ( value1 in D2.keys() ):
                      if ( id1 == D2[value1] ) : #a shared best reciprocal pair
                              self.SharedPairs[value1] = id1
      
      if (debug): self.SharedPairs 


   def output(self, outfile):      
      #outfl = open("_out.csv", "w")
      outfl = open( outfile, 'w')
      
      for k1 in self.SharedPairs.keys():
              line = k1 + '\t' + self.SharedPairs[k1] + '\n'
              outfl.write(line)
              
      outfl.close()
      
