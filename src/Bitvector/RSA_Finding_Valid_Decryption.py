import cvc5
from cvc5 import Kind

def findDecryptionExponent(P, Q, E, LOWER_BOUND, N, output=False):
    """ Finds a satisfying Decryption Exponent

    Args:
        P (int): Prime 1
        Q (int): Prime 2
        E (int): Encryption Exponent
        LOWER_BOUND (int): Lowest value the decryption exponent can be
        N (int): Bitwidth
        output (bool, optional): Print whether it was sat. Defaults to False.

    Returns:
        int: Decryption Exponent 
    """
    # ------------- SETUP -------------   
    tm = cvc5.TermManager()
    solver = cvc5.Solver(tm)
    
    solver.setLogic('QF_BV')
    solver.setOption("produce-models", "true")

    bitvectorN = solver.mkBitVectorSort(N)
    ONE  = solver.mkBitVector(N,1)

    # ------------- VARIABLE DECLARATIONS -------------   
    prime1 = tm.mkConst(bitvectorN, 'prime1')
    prime2 = tm.mkConst(bitvectorN, 'prime2')

    # Public and Private exponents
    encrypt = tm.mkConst(bitvectorN, 'encrypt')
    decrypt = tm.mkConst(bitvectorN, 'decrypt')

    # ------------- INPUT ASSERTIONS -------------   
    inputPredicate1 = tm.mkTerm(Kind.EQUAL, prime1, solver.mkBitVector(N, P))
    solver.assertFormula(inputPredicate1)

    inputPredicate2 = tm.mkTerm(Kind.EQUAL, prime2, solver.mkBitVector(N, Q))
    solver.assertFormula(inputPredicate2)
    
    inputPredicate3 = tm.mkTerm(Kind.EQUAL, encrypt, solver.mkBitVector(N, E))
    solver.assertFormula(inputPredicate3)

    # ------------- CONSTRAINTS -------------    
    # Rule: Decryption Exponent must be greater than 1
    d1 = tm.mkTerm(Kind.BITVECTOR_UGT, decrypt, ONE)
    solver.assertFormula(d1)

    # Rule: Exponent custom lower bound
    decrypt_lower_bound = tm.mkTerm(Kind.BITVECTOR_UGT, decrypt, solver.mkBitVector(N, LOWER_BOUND))
    solver.assertFormula(decrypt_lower_bound)

    # Calculate Euler totient function by (p-1)(q-1) 
    pminus1 = tm.mkTerm(Kind.BITVECTOR_SUB, prime1, ONE)
    qminus1 = tm.mkTerm(Kind.BITVECTOR_SUB, prime2, ONE)
    totientN = tm.mkTerm(Kind.BITVECTOR_MULT, pminus1, qminus1)

    # Rule: Exponents must be mutliplicative inverses of each other modulo totient n
    ed = tm.mkTerm(Kind.BITVECTOR_MULT, encrypt, decrypt)
    moduloED = tm.mkTerm(Kind.BITVECTOR_UREM, ed, totientN)
    moduloCongruence = tm.mkTerm(Kind.EQUAL, moduloED, ONE)
    solver.assertFormula(moduloCongruence)
    
    solver.checkSat()

    if output:
       print("Finding Decryption greater than "+str(LOWER_BOUND)+" was", solver.checkSat())

    return solver.getValue(tm.mkTerm(Kind.BITVECTOR_TO_NAT, decrypt))


if __name__ == '__main__':
    
    # ------------- INPUT -------------
    P = 11 
    Q = 13
    E = 23
    D_lower_bound  = 0 # D will be greater than this

    N = 6 # BITVECTOR LENGTH

    D = findDecryptionExponent(P,Q,E,D_lower_bound, N)

    print("A valid decryption number is:", D)
    