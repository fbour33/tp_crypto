import random
import sys
from math import sqrt
from common import *

####################
# Q9
####################

# input: n
# output: e,d,N
def gen_rsa(n):
    p, q = gen_prime(n), gen_prime(n)
    while p == q:
        q = gen_prime(n)
    N = p*q
    phi_N = (p-1)*(q-1)
    e = random.randint(2, phi_N-1)
    while pgcd(e, phi_N) != 1:
        e = random.randint(2, phi_N-1)
    d = inverse_modulaire(phi_N, e)
    return(e, d, N)

#print(gen_rsa(512))
    
####################
# Q10
####################    
    
# e exponent
# N modulo
# m message
# output: c
# message/cipher sous forme de nombre
def enc_rsa(m,e,N):
    return expo_modulaire_fast(e, m, N)

# d exponent
# N modulo
# c cipher 
# output m   
# message/cipher sous forme de nombre
def dec_rsa(c,d,N):
    return expo_modulaire_fast(d, c, N)

####################
# Q11
####################

#def cut_message(m, N):
#    len_m = len(m) 
#    nb_cut = len(m)//N
#    if(len_m%N != 0):
#        nb_cut += 1 
#    cuts = []
#    for i in range(nb_cut):
#        first = i*N 
#        end = first + N
#        cuts.append(m[first:end])
#    return cuts
    
# e exponent
# N modulo
# m message sous forme de texte
# output: c sous forme de nombre
def RSAcipher(e,N,m):
    m_int = str_to_int(m)
    if(m_int > N):
        raise ValueError("Il faut que N soit plus grand que str_to_int(m)")
    #assert(m_int > N, "Il faut N plus grand que m_int")
    #if(m_int > N):
    #    m_cut = cut_message(m, N)
    #    for i in range(len(m_cut)):
    #        m_cut[i] = int_to_str(enc_rsa(str_to_int(m_cut[i]), e, N))
    #    m_encrypt = ''.join(m_cut)
    #    m_int = str_to_int(m_encrypt)
    return enc_rsa(m_int, e, N)


# d exponent
# N modulo
# c cipher sous forme de nombre
# output: m message sous forme de texte
def RSAdecipher(d,N,c):
    # utilisez int_to_str
    #print("longueur de m ", len(m), "modulo :", N)
    if(c > N):
        raise ValueError("N doit être plus grand que c")
    #if(c > N):
    #    c_cut = cut_message(int_to_str(c), N)
    #    for i in range(c_cut):
    #        c_cut[i] = dec_rsa(str_to_int(c_cut[i]), d, N)
    #        print(c_cut)
    #    c_decrypt = ''.join(c_cut)
    #else:
    c_decrypt = dec_rsa(c, d, N)
    return int_to_str(c_decrypt)


####################
# Q13
####################

# d exponent
# N modulo
# m message sous forme de texte
# output: sig
def RSAsignature(d,N,m):
    return expo_modulaire_fast(d, str_to_int(m), N)

# e exponent
# N modulo
# m message sous forme de texte
# sig signature
# output: bool verifie si signature valide
# true = valid
def RSAverification(e,N,m,sig):
    return m == int_to_str(expo_modulaire_fast(e, sig, N))

