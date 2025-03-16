import cvc5
from cvc5 import Kind
import math

def isValidRSAConfiguration(P,Q,E,D, output=False):
    """Verifies input satisfies properties specified in RSA

    Args:
        P (int): Prime 1
        Q (int): Prime 2
        E (int): Encryption Exponent
        D (int): Decryption Exponent
        output (bool, optional): Print whether it was sat. Defaults to False.

    Returns:
        bool: whether it is a valid or not
    """
    # ------------- SETUP -------------   
    
    tm = cvc5.TermManager()
    solver = cvc5.Solver(tm)
    
    solver.setLogic('NIA')
    solver.setOption("produce-models", "true")
    solver.setOption("finite-model-find", "true")

    INT = solver.getIntegerSort()
    ZERO = solver.mkInteger(0)
    ONE = solver.mkInteger(1)

    # ------------- INPUT ASSERTIONS -------------   

    prime1 = tm.mkInteger(P)
    prime2 = tm.mkInteger(Q)
    encrypt = tm.mkInteger(E)
    decrypt = tm.mkInteger(D)
    
    # Calculate Euler totient function by (p-1)(q-1) 
    pminus1 = tm.mkTerm(Kind.SUB, prime1, ONE)
    qminus1 = tm.mkTerm(Kind.SUB, prime2, ONE)
    totientN = tm.mkTerm(Kind.MULT, pminus1, qminus1)

    # ------------- RULES -------------    

    # Rule: Input should be primes
    for i in range(2, math.ceil(P ** 0.5)+1):
        x = tm.mkInteger(i)
        remainder = solver.mkTerm(Kind.INTS_MODULUS, prime1, x)
        solver.assertFormula(solver.mkTerm(Kind.NOT, solver.mkTerm(Kind.EQUAL, remainder, ZERO)))

    for i in range(2, math.ceil(Q ** 0.5)+1):
        x = tm.mkInteger(i)
        remainder = solver.mkTerm(Kind.INTS_MODULUS, prime2, x)
        solver.assertFormula(solver.mkTerm(Kind.NOT, solver.mkTerm(Kind.EQUAL, remainder, ZERO)))

    # Rule: Primes are positive integers greater than 1
    p1 = tm.mkTerm(Kind.GT, prime1, ONE)
    solver.assertFormula(p1)

    p2 = tm.mkTerm(Kind.GT, prime2, ONE)
    solver.assertFormula(p2)

    # Rule: Primes should not be equal to each other
    p3 = tm.mkTerm(Kind.DISTINCT, prime1, prime2)
    solver.assertFormula(p3)

    # Rule: Exponents must be greater than 1
    e1 = tm.mkTerm(Kind.GT, encrypt, ONE)
    solver.assertFormula(e1)

    d1 = tm.mkTerm(Kind.GT, decrypt, ONE)
    solver.assertFormula(d1)

    # Rule: Encryption Exponent must be relatively prime to totient n
    cd = tm.mkConst(INT, 'commonDenominator')
    divideEncryption = tm.mkTerm(Kind.INTS_MODULUS, encrypt, cd)
    divideTotient = tm.mkTerm(Kind.INTS_MODULUS, totientN, cd)

    gcd = tm.mkConst(INT, 'greatestCommonDenominator')
    gcdDividesEncryption = tm.mkTerm(Kind.INTS_MODULUS, encrypt, gcd)
    gcdDividesTotient = tm.mkTerm(Kind.INTS_MODULUS, totientN, gcd)
    
    sameDivisor = tm.mkTerm(Kind.EQUAL, divideTotient, divideEncryption, ZERO)
    properDivisor = tm.mkTerm(Kind.GT, cd, ZERO)

    commonDivisorCondition = tm.mkTerm(Kind.AND, properDivisor, sameDivisor)

    solver.assertFormula(commonDivisorCondition)

    sameDivisor = tm.mkTerm(Kind.EQUAL, gcdDividesTotient, gcdDividesEncryption, ZERO)
    properDivisor = tm.mkTerm(Kind.GT, gcd, ZERO)

    greatestDivisor = tm.mkTerm(Kind.GEQ, gcd, cd)
    isRelativelyPrime = tm.mkTerm(Kind.EQUAL, gcd, ONE)

    greatestCommonDivisorCondition = tm.mkTerm(Kind.AND, properDivisor,sameDivisor,greatestDivisor, isRelativelyPrime)

    solver.assertFormula(greatestCommonDivisorCondition)

    # Rule: Exponents must be multiplicative inverses of each other modulo totient n
    ed = tm.mkTerm(Kind.MULT, encrypt, decrypt)
    moduloED = tm.mkTerm(Kind.INTS_MODULUS, ed, totientN)
    moduloCongruence = tm.mkTerm(Kind.EQUAL, moduloED, ONE)

    solver.assertFormula(moduloCongruence)

    results = str(solver.checkSat())

    if output:
        print("RSA Configuration was:", solver.checkSat())

    if results == "sat":
        return True

    return False
    
if __name__ == '__main__':
    # ------------- INPUT -------------
    P = 11 
    Q = 13
    E = 23 
    D = 47

    b = isValidRSAConfiguration(P,Q,E,D)

    if b:
        print("This is a valid configuration")    
    else:
        print("This is not a valid configuration")    

