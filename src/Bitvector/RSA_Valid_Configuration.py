import math
import cvc5
from cvc5 import Kind

def isValidRSAConfiguration(P,Q,E,D, N, output=False):
    """Verifies input satisfies properties specified in RSA

    Args:
        P (int): Prime 1
        Q (int): Prime 2
        E (int): Encryption Exponent
        D (int): Decryption Exponent
        N (int): BITWIDTH
        output (bool, optional): Print whether it was sat. Defaults to False.

    Returns:
        bool: whether it is a valid or not
    """

    assert(len(bin(P*Q)[2:]) <= N), "Modulus can't fit in "+str(N)+" bits"
    assert(len(bin(E)[2:]) <= N), "Encryption Exponent can't fit in "+str(N)+" bits"
    assert(len(bin(D)[2:]) <= N), "Decryption Exponent can't fit in "+str(N)+" bits"

    # ------------- SETUP -------------   
    tm = cvc5.TermManager()
    solver = cvc5.Solver(tm)
    
    solver.setLogic('QF_BV')
    solver.setOption("produce-models", "true")

    bitvectorN = solver.mkBitVectorSort(N)
    ZERO  = solver.mkBitVector(N,0)
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

    inputPredicate4 = tm.mkTerm(Kind.EQUAL, decrypt, solver.mkBitVector(N, D))
    solver.assertFormula(inputPredicate4)

    # ------------- Constraints -------------    

    # Rule: Input should be primes
    for i in range(2, math.ceil(P ** 0.5)+1):
        x = tm.mkBitVector(N, i)
        remainder = solver.mkTerm(Kind.BITVECTOR_UREM, prime1, x)
        solver.assertFormula(solver.mkTerm(Kind.NOT, solver.mkTerm(Kind.EQUAL, remainder, ZERO)))

    for i in range(2, math.ceil(Q ** 0.5)+1):
        x = tm.mkBitVector(N, i)
        remainder = solver.mkTerm(Kind.BITVECTOR_UREM, prime2, x)
        solver.assertFormula(solver.mkTerm(Kind.NOT, solver.mkTerm(Kind.EQUAL, remainder, ZERO)))

    # Rule: Primes are positive integers greater than 1
    p1 = tm.mkTerm(Kind.BITVECTOR_UGT, prime1, ONE)
    solver.assertFormula(p1)

    p2 = tm.mkTerm(Kind.BITVECTOR_UGT, prime2, ONE)
    solver.assertFormula(p2)

    # Rule: Primes should not be equal to each other
    p3 = tm.mkTerm(Kind.DISTINCT, prime1, prime2)
    solver.assertFormula(p3)

    # Rule: Expononts must be greater than 1
    e1 = tm.mkTerm(Kind.BITVECTOR_UGT, encrypt, ONE)
    solver.assertFormula(e1)

    d1 = tm.mkTerm(Kind.BITVECTOR_UGT, decrypt, ONE)
    solver.assertFormula(d1)

    # Calculate Euler totient function by (p-1)(q-1) 
    pminus1 = tm.mkTerm(Kind.BITVECTOR_SUB, prime1, ONE)
    qminus1 = tm.mkTerm(Kind.BITVECTOR_SUB, prime2, ONE)
    totientN = tm.mkTerm(Kind.BITVECTOR_MULT, pminus1, qminus1)

    # TODO: DO EUCLIDEAN DIVISION ALGORITHM
    # Rule: Encryption Exponont must be relatively prime to totient n
    cd = tm.mkConst(bitvectorN, 'commonDenominator')
    divideEncryption = tm.mkTerm(Kind.BITVECTOR_UREM, encrypt, cd)
    divideTotient = tm.mkTerm(Kind.BITVECTOR_UREM, totientN, cd)

    gcd = tm.mkConst(bitvectorN, 'greatestCommonDenominator')
    gcdDividesEncryption = tm.mkTerm(Kind.BITVECTOR_UREM, encrypt, gcd)
    gcdDividesTotient = tm.mkTerm(Kind.BITVECTOR_UREM, totientN, gcd)

    sameDivisor = tm.mkTerm(Kind.EQUAL, divideTotient, divideEncryption, ZERO)
    properDivisor = tm.mkTerm(Kind.BITVECTOR_UGT, cd, ZERO)

    commonDivisorCondition = tm.mkTerm(Kind.AND, properDivisor, sameDivisor)

    sameDivisor = tm.mkTerm(Kind.EQUAL, gcdDividesTotient, gcdDividesEncryption, ZERO)
    properDivisor = tm.mkTerm(Kind.BITVECTOR_UGT, gcd, ZERO)

    greatestDivisor = tm.mkTerm(Kind.BITVECTOR_UGE, gcd, cd)
    isRelativelyPrime = tm.mkTerm(Kind.EQUAL, gcd, ONE)

    greatestCommonDivisorCondition = tm.mkTerm(Kind.AND, properDivisor,sameDivisor,commonDivisorCondition, greatestDivisor, isRelativelyPrime)

    solver.assertFormula(greatestCommonDivisorCondition)

    # Rule: Encryption Exponent and Decryption Exponent must be multiplicative inverses modulo totient n
    ed = tm.mkTerm(Kind.BITVECTOR_MULT, encrypt, decrypt)
    moduloED = tm.mkTerm(Kind.BITVECTOR_UREM, ed, totientN)
    moduloCongruence = tm.mkTerm(Kind.EQUAL, moduloED, ONE)
    solver.assertFormula(moduloCongruence)
    
    results = str(solver.checkSat())

    if output:
        print("RSA Configuration was: ", solver.checkSat())

    if results == "sat":
        return True

    return False


if __name__ == '__main__':
    
    # ------------- INPUT -------------
    P = 11 
    Q = 13
    E = 23 
    D = 47

    N = 32 # BITVECTOR LENGTH

    D = isValidRSAConfiguration(P,Q,E,D, N)

    if D:
        print("This is a valid configuration")    
    else:
        print("This is not a valid configuration")    
