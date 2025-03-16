"""
RSA SINGLE RANDOM VERIFICATION COMPARISON

This checks a single RSA keypair using RSA Library 

THE PARAMETERS ARE 
    - BITWIDTH_MAX: This is the Bitwidth size for the RSA key
"""

import csv
import math
import os
import sympy
import time
from tqdm import tqdm
import rsa

from src.Integer.RSA_Valid_Configuration import isValidRSAConfiguration as intValid
from src.Bitvector.RSA_Valid_Configuration import isValidRSAConfiguration as bvValid

# --------------- PARAMETERS --------------------

BITWIDTH_MAX = 32

(e,d) = rsa.newkeys(BITWIDTH_MAX)

P = d.p
Q = d.q
E = e.e
D = d.d

# --------------- EXPERIMENT --------------------

for ty in ["Bitvector", "Integer"]:
    if ty == "Integer":
        start = time.time()

        d = intValid(P,Q,E,D)

        end = time.time()
        
    elif ty == "Bitvector":
        start = time.time()

        d = bvValid(P,Q,E,D,BITWIDTH_MAX*2)

        end = time.time()

                        
    total_time = end-start
    print("Theory:",ty, ", Time", total_time, ", Was It correct", d )