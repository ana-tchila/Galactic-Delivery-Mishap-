
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

        # Creates an empty list to store hash positions 
        digests = []

        # Iterates through multiple hash functions
        for i in range(self.hash_count): 

            digest = mmh3.hash(item, i) %self.size 
            #Hashes the item 
            #Uses different original values to simulate 
            #Multiple hash function 
            #Makes sure the hash value 
            #fits the bit array size 
            
            digests.append(digest)
            # Stores the hash positions in the list 

            self.bit_array[digest] = True
            # Sets the corresponding bit positions to True 
    
    def check(self, item): 
        """ Checks if an item is present""" 

        for i in range(self.hash_count): # Iterates through 

            digest = mmh3.hash(item,i) % self.size #Hashes 

            if self.bit_array[digest] == False: #Checks if any bit position is False 

                return False # Returns False 

        return True # Returns True 

    @classmethod 
    def get_size(self, n, p): 
        """ 
        Returns the size of the bit array

        args: 
            n: number of expected items 
            p: false positive probability

        output: 
            int: Size of the bit array 
        """

        #Formula for calculating the array size
        m = -(n * math.log(p))/(math.log(2) ** 2) 

        return int(m) #Returns m in integer form 
    
    @classmethod
    def get_hash_count(self, m, n): 
        """ Returns the number of hash functions used 

        Args:
            m: size of the bit array 
            n: number of expected items 
        Output: 
            int: Hash function count 
        """ 
        
        #Formula for calculating hash function count
        k = (m/n) * math.log(2)

        return int(k) # Returns k in integer form 

# Testing Class methods 
#print(BloomFilter.get_size(10, 0.01)) 
#print(BloomFilter.get_hash_count(95, 10))

def generate_licence(): 
    """Generates a random 5-digit licence."""

    return str(random.randint(10000, 99999)) # Generates random 5 digit numbers 

#Generates 10 licences 
all_licences = [generate_licence() for i in range(10)]

#Choose 5 Licences to be valid 
valid_licences = random.sample(all_licences, 5) 
licence_filter = BloomFilter(len(valid_licences), 0.01) #Make an instance 

#Add only the valid licenses into the Bloom Filter 
for licence in valid_licences: 
    licence_filter.add(licence) 

#Assigns the player one random licence 
player_licence = random.choice(all_licences)

def police_scan(licence): 
    """Checks if a licence is valid"""

    if licence_filter.check(licence): 
        return "Let the driver pass"
    else: 
        return "Access denied" 

#Test run 
#print(police_scan(player_licence))

#5740479 
