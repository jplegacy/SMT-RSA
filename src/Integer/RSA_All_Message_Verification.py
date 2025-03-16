import cvc5
from cvc5 import Kind

from RSA_Valid_Configuration import isValidRSAConfiguration


def allMessageDecryptEncryptVerification(P,Q,E,D, output=False):
    """ Verifies every message remains the same after encryption and decryption

    Args:
        P (int): Prime 1
        Q (int): Prime 2
        E (int): Encryption Exponent
        D (int): Decryption Exponent
        output (bool, optional): Print whether it sat. Defaults to False.

    Returns:
        bool: Whether all messages remain the same
    """
    
    # ------------- SETUP -------------   
    
    tm = cvc5.TermManager()
    solver = cvc5.Solver(tm)
    
    solver.setLogic('NIA')
    solver.setOption("produce-models", "true")
    solver.setOption("finite-model-find", "true")

    INT = solver.getIntegerSort()

    # ------------- VARIABLE DECLARATIONS -------------   
    
    prime1 = tm.mkConst(INT, 'prime1')
    prime2 = tm.mkConst(INT, 'prime2')

    encrypt = tm.mkConst(INT, 'encrypt')
    decrypt = tm.mkConst(INT, 'decrypt')

    # ------------- INPUT ASSERTIONS -------------   
    prime1 = tm.mkInteger(P)
    prime2 = tm.mkInteger(Q)
    encrypt = tm.mkInteger(E)
    decrypt = tm.mkInteger(D)
    
    modulus = tm.mkTerm(Kind.MULT, prime1, prime2)
    ed = tm.mkTerm(Kind.MULT, encrypt, decrypt)

    r = isValidRSAConfiguration(P,Q,E,D)
    solver.assertFormula(tm.mkBoolean(r))

    for i in range(0, P*Q):
        cipherDecryptPower = tm.mkTerm(Kind.POW, tm.mkInteger(i), ed)
        moduloPower = tm.mkTerm(Kind.INTS_MODULUS , cipherDecryptPower, modulus)
        messageCongruence = tm.mkTerm(Kind.EQUAL, tm.mkInteger(i), moduloPower)

        solver.assertFormula(messageCongruence)

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

    b = allMessageDecryptEncryptVerification(P,Q,E,D)

    print("Messages are preserved:", b)    

