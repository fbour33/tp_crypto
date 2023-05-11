import random
import sys
from math import sqrt


####################
# Q1
####################

# retourne le pgcd de deux entiers naturels
def pgcd(a, b):
    while b != 0:
        r = a % b
        a = b
        b = r
    return a

# algo euclide etendu
# retourne d,u,v avec pgcd(a,b)=d=ua+vb
def euclide_ext(a,b):
    u, v = 0, 1
    u_prec, v_prec = 1, 0
    while b != 0:
        q = a//b
        r = a%b
        a, b = b, r
        u_prec, u = u, u_prec-q*u
        v_prec, v = v, v_prec-q*v
    return (a, u_prec, v_prec)
        
#print(euclide_ext(1027, 712))
    
####################
# Q2
####################

# retourne un entier b dans [1,N-1] avec ab=1 modulo N
def inverse_modulaire(N,a):
    d, u, v = euclide_ext(a, N)
    if(d != 1):
        raise ValueError("d != 1")
    if v < 0:
        return v+N
    return v #Peut être remplacer par u%N

#print(inverse_modulaire(712, 1027))

####################
# Q3
####################

# retourne (b**e) % n
# calcule le modulo apres chaque multiplication
def expo_modulaire(e,b,n):
    res = b
    for _ in range(1, e):
        res *= b
        res = res%n
    #if res < 0:
    #    res += n
    return res

#print(expo_modulaire(3, 5, 13))

####################
# Q4
####################

# retourne (b**e) % n
# calcule le modulo apres chaque multiplication
# O(log(e)) operations
def expo_modulaire_fast(e,b,n):
    # help:
    
    # representer e en binaire
    #bin_e = bin(e)[2:]
    
    # utile pour iterer sur chaque element de e
    #for x in range(len(bin_e)):
    #   int(bin_e[x])
    
    bin_e = bin(e)[2:]
    res = 1
    b = b%n
    for x in range(len(bin_e)):
        int_e = int(bin_e[-x-1])
        if(int_e == 1):
            res = (res*b)%n
        b = (b*b)%n
    #if res < 0:
    #    res += n
    return res

print(expo_modulaire_fast(3, 5, 13))

####################
# Q5
####################

# retourne la liste des nombres premiers <= n
# methode du crible d Eratosthene
def crible_eras(n):
    primes = []
    is_prime = [True] * (n+1) # initialement tous sont considérés premiers
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i**2, n+1, i):
                is_prime[j] = False
    for i in range(int(n**0.5)+1, n+1):
        if is_prime[i]:
            primes.append(i)
    return primes
        
####################
# Q6
####################

# input: n  
# input: t number of tests
# test if prime according to fermat
# output: bool if prime 
def test_fermat(n,t):
    if t <= 0:
        return True
    # random number generator between a and b
    #x = random.randint(a,b)
    for i in range(t):
        a = random.randint(2, n-1)
        if expo_modulaire_fast(n-1, a, n) != 1:
            return False
    return True

#print(test_fermat(18, 5))

####################
# Q7
####################

# input: n
# output: r and u coefficient
# for rabin test 
# returns r,u such that 2^r * u = n and u is odd
def find_ru(n):
    r = 0
    n -= 1
    while n%2 == 0:
        r += 1
        n = n//2
    return r,n

####################
# Q8
####################

#n entier
#a entier dans [1,n-2]
#pgcd(a,n)=1
#retourne True , si a est un temoin de Rabin de non-primalite de n
def temoin_rabin(a,n):
    # utilisez expo_modulaire_fast !
    r,u = find_ru(n)
    x = expo_modulaire_fast(u,a,n)
    if x == 1:
        return False
    for i in range(r+1):
        tmp = expo_modulaire_fast((2**i)*u, a, n)
        if tmp == -1 or tmp == n-1:
            return False
    return True

# for i in range(20):
#     print(i," : ", temoin_rabin(i, 71))

#n entier a tester, t nombre de tests
#retourne True , si n est premier
#retourne False , avec proba > 1-(1/4)**t, si n est compose
def test_rabin(n,t):
    for i in range(t):
        rand = random.randint(1, n)
        tmp = temoin_rabin(rand,n)
        if tmp == True:
            return False
    return True

# print(test_rabin(163, 10))
            
# prime generator
# output: n range for prime number
# utilise votre implementation de rabin (ou la plus effice si rabin non dispo)
# pour generer un nombre premier sur n bits.
# range de n: p = random.randint(pow(2,n-1),pow(2,n)-1)
def gen_prime(n):
    while True:
        p = random.randint(pow(2, n-1), pow(2, n)-1)
        if test_rabin(p, 20): # t = 20 pour une probabilité d'erreur très faible
            return p

# print(gen_prime(10))

####################
# Helper functions for rsa/elgamal
####################

# Helper function
# convert str to int
def str_to_int(m):
    s = 0
    b = 1
    for i in range(len(m)):
        s = s + ord(m[i])*b
        b = b * 256
    return s

# Helper function
# convert int to str
def int_to_str(c):
    s = ""
    q,r = divmod(c,256)
    s = s+str(chr(r))
    while q != 0:
        q,r = divmod(q,256)
        s = s+str(chr(r))
    return s
