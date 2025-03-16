"""
RSA DECRYPTION KEY GENERATION RUNTIME COMPARISON

This experiment times how fast CVC5 Bitvectors, CVC5 Integers, and native python can run
findDecryptionExponent on a number of fixed of parameters 
 
THE PARAMETERS ARE 
    - NUM_OF_EXPERIMENTS: Number of many experiments 

    - LOWER_BOUND: A lower-bound on the decryption key value
        Setting this lets you check how they perform with handling bigger numbers
    
    - BITWIDTH_MAX: This is the Bitwidth size for bitvectors
        (Disclaimer - If the bitwidth is too small, it will crash during the experiment)

    - DATA_DIRECTORY: This specifies the path where the experiement will dump its data
        Right now, the name schema is
            <type>_e<NUM_OF_EXPERIMENTS>d<LOWER_BOUND>b<BITWIDTH_MAX>.csv
"""

import csv
import os
import sympy
import time
from tqdm import tqdm

from src.Python.RSA_Finding_Valid_Decryption import findDecryptionExponent as pyFindDecrypt
from src.Integer.RSA_Finding_Valid_Decryption import findDecryptionExponent as intFindDecrypt
from src.Bitvector.RSA_Finding_Valid_Decryption import findDecryptionExponent as bvFindDecrypt

# --------------- PARAMETERS --------------------

NUM_OF_EXPERIMENTS = 1000

LOWER_BOUND = 0
BITWIDTH_MAX = 64
DATA_DIRECTORY = "./data/EncryptionRace/e"+str(NUM_OF_EXPERIMENTS) + "d"+str(LOWER_BOUND)+"/"

# --------------- MAKE FOLDER --------------------

try:
    os.makedirs(DATA_DIRECTORY)
except FileExistsError:
    pass

# --------------- GET PRIME NUMBERS --------------------

primes = [sympy.prime(i) for i in range(1, NUM_OF_EXPERIMENTS+3)]

# --------------- EXPERIMENT --------------------

for ty in ["Python", "Bitvector", "Integer"]:
    DATA_FILE = DATA_DIRECTORY + ty+"_e" + str(NUM_OF_EXPERIMENTS) + "d"+str(LOWER_BOUND)+"b"+str(BITWIDTH_MAX)+".csv"

    all_times = []
    decryption_keys= []

    for i in tqdm(range(NUM_OF_EXPERIMENTS)):
        # CONSEQUTATIVE WINDOW
        P = primes[i]
        Q = primes[(i+1)]
        E = primes[(i+2)]

        # FORWARD SPLIT WINDOW + Standard Exponent
        # P = primes[i]
        # E = primes[i+1] 
        # Q = primes[(i+ ((len(primes)-i)//2)+1) % len(primes)]


        if ty == "Python":
            start = time.time()

            d = pyFindDecrypt(P,Q,E, LOWER_BOUND)

            end = time.time()

        elif ty == "Integer":
            start = time.time()

            d = intFindDecrypt(P,Q,E, LOWER_BOUND)

            end = time.time()
            
        elif ty == "Bitvector":
            start = time.time()

            d = bvFindDecrypt(P,Q,E, LOWER_BOUND, BITWIDTH_MAX)

            end = time.time()

        total_time = end-start
        all_times.append(total_time)
        decryption_keys.append(d)

    print("DONE "+ty+" EXPERIEMENTS")

    with open(DATA_FILE, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["type","clock_time","P", "Q","E", "calculated_D"])
        for i, t in enumerate(all_times):
            writer.writerow([ty,t,primes[i],primes[i+1],primes[i+2], decryption_keys[i]])