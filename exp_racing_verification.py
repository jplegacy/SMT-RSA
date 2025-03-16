"""
RSA VERIFICATION RUNTIME COMPARISON

This experiment times how fast Bitvectors and Integers
can check all possible inputs to the isValidRSAConfiguration
from the range 0-INTEGER_BOUND

That is, for all isValidRSAConfiguration(i,j,k,l) where i,j,k,l in range(0,INTEGER_BOUND)
    Meaning the runtime of this experiment is INTEGER_BOUND^4
    
THE PARAMETERS ARE 
    - INTEGER_BOUND: How many inputs should be covered 

    - BITWIDTH_MAX: This is the Bitwidth size for bitvectors
        (Disclaimer - If the bitwidth is too small, it will crash during the experiment)

    - DATA_DIRECTORY: This specifies the path where the experiment will dump its data
        Right now, the name schema of each file is
            <type>_bound<INTEGER_BOUND>bw<BITWIDTH_MAX>.csv
"""

import csv
import os
import sympy
import time
from tqdm import tqdm

from src.Integer.RSA_Valid_Configuration import isValidRSAConfiguration as intValid
from Bitvector.RSA_Valid_Configuration import isValidRSAConfiguration as bvValid

# --------------- PARAMETERS --------------------

INTEGER_BOUND = 30 #CHECKS ALL INPUTS FROM 0-IB^4 
BITWIDTH_MAX = 16
DATA_DIRECTORY = "./data/VerificationRace/bound"+str(INTEGER_BOUND) + "bw"+str(BITWIDTH_MAX)+"/"

# --------------- MAKE FOLDER --------------------
try:
    os.makedirs(DATA_DIRECTORY)
except FileExistsError:
    pass

# --------------- EXPERIMENT --------------------

for ty in ["Bitvector", "Integer"]:
    DATA_FILE = DATA_DIRECTORY + ty+"_bound" + str(INTEGER_BOUND) + "bw"+str(BITWIDTH_MAX)+".csv"

    all_times = []
    inputs= []
    answers = []

    for i in tqdm(range(INTEGER_BOUND)):
        for j in range(INTEGER_BOUND):
            for k in range(INTEGER_BOUND):
                for l in range(INTEGER_BOUND):
                    if ty == "Integer":
                        start = time.time()

                        d = intValid(i,j,k,l)

                        end = time.time()
                        
                    elif ty == "Bitvector":
                        start = time.time()

                        d = bvValid(i,j,k,l, BITWIDTH_MAX)

                        end = time.time()

                        
                    total_time = end-start
                    all_times.append(total_time)
                    inputs.append((i,j,k,l))
                    answers.append(d)

    print("DONE "+ty+" EXPERIEMENTS")

    with open(DATA_FILE, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["type","clock_time","P", "Q","E", "D", "Answers"])
        for i, t in enumerate(all_times):
            inp = inputs[i]
            writer.writerow([ty,t,inp[0],inp[1],inp[2], inp[3], answers[i]])