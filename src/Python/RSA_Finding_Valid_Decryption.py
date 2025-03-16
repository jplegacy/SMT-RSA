import cvc5
from cvc5 import Kind
import math

def findDecryptionExponent(P,Q,E,LOWER_BOUND=0, print=False):

    assert(P*Q), "unsat"
    
    # Rule: Primes are positive integers greater than 1
    assert(P>1), "unsat"
    assert(Q>1), "unsat"

    # Rule: Primes should not be equal to each other
    assert(not (P == Q)), "unsat"
    
    # Rule: Expononts must be greater than 1
    assert(E>1), "unsat"

    totientN = (P-1) * (Q-1)
    
    # Rule: Encryption Exponont must be relatively prime to totient n
    assert(math.gcd(E, totientN) == 1),  "unsat "+str(P)+" "+str(Q)+" "+str(E)

    d = 1
    if(LOWER_BOUND):  
        d = LOWER_BOUND 

    while(d > 0):
        if math.gcd(d*E, totientN) > 1:
            d += 1
            continue

        break
    
    if print:
       print("Finding Decryption greater than "+str(LOWER_BOUND)+" was", "sat")
    return d
    

if __name__ == '__main__':
    
    # ------------- INPUT -------------
    P = 11 
    Q = 13
    E = 23 
    D_lower_bound  = 2000012223200 # D will be greater than this

    D = findDecryptionExponent(P,Q,E,D_lower_bound)

    print("A valid decryption number is: ", D)
    

