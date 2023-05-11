import random
import sys
from math import sqrt, ceil
from common import *

####################
# Q14
####################

# retourne p g 
# g generateur sur le groupe Z*p => on utilise 3
# p premier sur n bits.

def facteurs(n):
    """Renvoie la liste des diviseurs de n."""
    diviseurs = []
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            diviseurs.append(i)
            if i != n // i:
                diviseurs.append(n // i)
    diviseurs.sort()
    return diviseurs

# print(facteurs(786))

def gen_ElGamal_pg(n):
    p = gen_prime(n)
    facteur = facteurs(p-1)
    while True:
        g = random.randint(2, p-1)
        is_generator = True
        for q in facteur:
            h = expo_modulaire_fast(int((p-1)/q), g, p)
            if h == 1:
                is_generator = False
                break
        if is_generator:
            return (p, g)

####################
# Q15
####################

# retourne couple cle prive/publique [sk,pk]
# definit tel que sk compris entre (3,p-2) 
# pk =  g^sk [p]
# output: [sk,pk]
def gen_elgamal_sk_pk(p,g):
    sk = random.randint(3, p-2)
    pk = expo_modulaire_fast(sk, g, p)
    return (sk, pk)

####################
# Q16
####################
    
# pk_a,sk_a,pk_b,sk_b sont les cles publiques prive de A B modulo p
# retourne le secret partage par A et B
def gen_elgamal_get_secret(pk_a,sk_a,pk_b,sk_b,p):
    s1 = expo_modulaire_fast(sk_a, pk_b, p)
    s2 = expo_modulaire_fast(sk_b, pk_a, p)
    assert s1 == s2
    return s1

####################
# Q17
####################

# chiffrement du message m avec le secret
# output: chaine de charactere c en binaire  represantant c 
# cotrainte: secret plus grand que message 
def enc_elgamal(m,secret,p):
    # indice transormez le message (et le secret en binaire) en binaire:
    # bin_m = bin(str_to_int(m))[2:]  
    m = str_to_int(m)
    assert secret > m
    c = (m*secret)%p
    return int_to_str(c)

# dechiffrement du message c avec le secret
# output: chaine de charactere m 
# cotrainte: secret plus grand que message
def dec_elgamal(c,secret,p):
    c = str_to_int(c)
    tmp = inverse_modulaire(p, secret)
    m = (c*tmp)%p
    return int_to_str(m)

####################
# Q19
####################
 
# retourne la signatue [r, s]
# sk cle secrete utilise pour signer message m
# m sous forme de texte     
def elgamalsignature(g,p,sk,m):
    m = str_to_int(m)
    while True:
        k = random.randint(1, p-2)
        if pgcd(k, p-1) == 1:
            break
    u = expo_modulaire_fast(k, g, p)
    tmp = m -u*sk
    k = inverse_modulaire(p-1, k)
    v = (tmp*k)%p
    return (u,v)
    
# r,s signature
# pk cle publique utilise pour signer message m
# m sous forme de texte 
# output: bool verifie si signature valide
# true = valid  
def elgamalverification(g,p,r,s,m,pk):
    m = str_to_int(m)
    a1 = expo_modulaire_fast(m, g, p)
    a2 = expo_modulaire_fast(r, pk, p)
    a3 = expo_modulaire_fast(s, r, p)
    test = (a1-a2*a3)%p
    return test