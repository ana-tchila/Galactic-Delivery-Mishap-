#5740479 
 
#Police Station Node 
 
import math 
import mmh3
import random 
from bitarray import bitarray 
 
 
class BloomFilter(object): 
    """Class for bloom filter
    
    This implementation uses: 
    - MurmurHash3 Hash functions 
    - A bit array
    """ 
    def __init__(self, items_count, fp_prob): 
        """ Constructor for Bloom filter 
 
        Args: 
        items_count: Number of items expected to be stored. 
        fp_prob :Desired false positive probability
        """ 
        self.fp_prob = fp_prob # Stores false positive probability 
 
        # Size of the bit array needed 
        self.size = self.get_size(items_count, fp_prob)
        self.bit_array = bitarray(self.size) #Creates the bit array 
        self.bit_array.setall(0) # Set all the bits to zero 
 
        #Number of hash function needed 
        self.hash_count = self.get_hash_count(self.size, items_count) 
    
    def add(self, item): 
        """ Adds an item in the filter""" 

        digests = []
 
        for i in range(self.hash_count): 
 
            digest = mmh3.hash(item, i) % self.size 
            digests.append(digest)
            self.bit_array[digest] = True
    
    def check(self, item): 
        """ Checks if an item is present""" 
 
        for i in range(self.hash_count):
 
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:
 
                return False
 
        return True
 
    @classmethod 
    def get_size(self, n, p): 
        """ Returns the size of the bit array """
 
        m = -(n * math.log(p))/(math.log(2) ** 2) 
 
        return int(m)
    
    @classmethod
    def get_hash_count(self, m, n): 
        """ Returns the number of hash functions used """ 
        
        k = (m/n) * math.log(2)
 
        return int(k)
 
 
def generate_licence(): 
    """Generates a random 5-digit licence."""
 
    return str(random.randint(10000, 99999))
 
 
# Generates 10 licences
all_licences = [generate_licence() for i in range(10)]
 
# Choose 5 licences to be valid
valid_licences = random.sample(all_licences, 5)
licence_filter = BloomFilter(len(valid_licences), 0.01)
 
# Add only the valid licences into the Bloom Filter
for licence in valid_licences:
    licence_filter.add(licence)
 
# player_licence starts as None — the player picks their own in the game
player_licence = None
 
 
def police_scan(licence): 
    """Checks if a licence is valid using the Bloom Filter."""
 
    if licence_filter.check(licence): 
        return "Let the driver pass"
    else: 
        return "Access denied"
 
#5740479
