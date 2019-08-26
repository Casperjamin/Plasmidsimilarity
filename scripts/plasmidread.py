
from Bio import seqIO

class plasmid:
	def __init__(self, sequence, ID):
		self.sequence = str(sequence).UPPER()
		self.ID = ID
        self.length = len(self.sequence)


    def kmerrize(k = 31):
        
