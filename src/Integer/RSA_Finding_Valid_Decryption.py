import math
import cvc5
from cvc5 import Kind


def findDecryptionExponent(P,Q,E,LOWER_BOUND, output=False):
    """ Finds a satisfying Decryption Exponent

    ASSUMES THE FOLLOWING:
    - P,Q ARE INTS
    - P,Q,E > 1
    - P != Q
    - GCD(E,(P-1)*(Q-1))
    
    Args:
        P (int): Prime 1
        Q (int): Prime 2
        E (int): Encryption Exponent
        LOWER_BOUND (int): Lowest value the decryption exponent can be
        output (bool, optional): Print whether it was sat. Defaults to False.

    Returns:
        int: Decryption Exponent 
    """    
    # ------------- SETUP -------------   
    
    tm = cvc5.TermManager()
    solver = cvc5.Solver(tm)
    
    solver.setLogic('QF_NIA')
    solver.setOption("produce-models", "true")

    INT = solver.getIntegerSort()
    ONE = solver.mkInteger(1)

    # ------------- VARIABLE DECLARATIONS -------------   
    
    prime1 = tm.mkConst(INT, 'prime1')
    prime2 = tm.mkConst(INT, 'prime2')

    # Public and Private exponents
    encrypt = tm.mkConst(INT, 'encrypt')
    decrypt = tm.mkConst(INT, 'decrypt')

    # ------------- INPUT ASSERTIONS -------------   

    inputPredicate1 = tm.mkTerm(Kind.EQUAL, prime1, solver.mkInteger(P))
    solver.assertFormula(inputPredicate1)

    inputPredicate2 = tm.mkTerm(Kind.EQUAL, prime2, solver.mkInteger(Q))
    solver.assertFormula(inputPredicate2)
    
    inputPredicate3 = tm.mkTerm(Kind.EQUAL, encrypt, solver.mkInteger(E))
    solver.assertFormula(inputPredicate3)

    # ------------- CONSTRAINTS -------------    

    # Rule: Decrypt Exponent must be greater than 1
    d1 = tm.mkTerm(Kind.GT, decrypt, ONE)
    solver.assertFormula(d1)

    # Rule: Exponent custom lower bound
    decrypt_lower_bound = tm.mkTerm(Kind.GT, decrypt, solver.mkInteger(LOWER_BOUND))
    solver.assertFormula(decrypt_lower_bound)

    # Calculate Euler totient function by (p-1)(q-1) 
    pminus1 = tm.mkTerm(Kind.SUB, prime1, ONE)
    qminus1 = tm.mkTerm(Kind.SUB, prime2, ONE)
    totientN = tm.mkTerm(Kind.MULT, pminus1, qminus1)

    # Rule: Exponents must be mutliplicative inverses of each other modulo totient n
    ed = tm.mkTerm(Kind.MULT, encrypt, decrypt)
    moduloED = tm.mkTerm(Kind.INTS_MODULUS, ed, totientN)
    moduloCongruence = tm.mkTerm(Kind.EQUAL, moduloED, ONE)

    solver.assertFormula(moduloCongruence)

    solver.checkSat()

    if output:
       print("Finding Decryption greater than "+str(LOWER_BOUND)+" was", solver.checkSat())

    return solver.getValue(decrypt)
    

if __name__ == '__main__':
    
    # ------------- INPUT -------------
    P = 11 
    Q = 13
    E = 23 
    D_lower_bound  = 20 # Decryption Exponent will be greater than or equal to this

    D = findDecryptionExponent(P,Q,E,D_lower_bound)

    print("A valid decryption number is:", D)
    

