import numpy as np
from PIL import Image

def logistic_map(x, r):
    return r*x*(1-x)

def gen_logistic_map(x0, r, n):
    x = x0
    for i in range(n):
        x = logistic_map(x, r)
        yield x

def gen_vals(x0, r, M, N):
    res = [[0 for i in range(N)] for j in range(M)]
    gen = gen_logistic_map(x0, r, M*N)
    for i in range(M):
        for j in range(N):
            res[i][j] = next(gen)
    return res

def encrypt(img, x0, r):
    M,N = img.size
    vals = gen_vals(x0, r, M, N)
    vals = [[int(i*256) for i in j] for j in vals]
    encrypted = [[img.getpixel((i,j)) for i in range(M)] for j in range(N)]
    shift = [sum(i)%N for i in vals]
    for i in range(M):
        encrypted[i] = encrypted[i][shift[i]:] + encrypted[i][:shift[i]]
    try:
        for i in range(M):
            for j in range(N):
                encrypted[i][j] = tuple(x^vals[i][j] for x in encrypted[i][j])
    except TypeError: # in case of greyscale
        for i in range(M):
            for j in range(N):
                encrypted[i][j] = encrypted[i][j]^vals[i][j]
    return Image.fromarray(np.array(encrypted, dtype=np.uint8))

def decrypt(img, x0, r):
    M,N = img.size
    vals = gen_vals(x0, r, M, N)
    vals = [[int(i*256) for i in j] for j in vals]
    decrypted = [[img.getpixel((i,j)) for i in range(M)] for j in range(N)]
    shift = [-sum(i)%N for i in vals]
    try: 
        for i in range(M):
            for j in range(N):
                decrypted[i][j] = tuple(x^vals[i][j] for x in decrypted[i][j])
    except TypeError: # in case of greyscale
        for i in range(M):
            for j in range(N):
                decrypted[i][j] = decrypted[i][j]^vals[i][j]
    for i in range(M):
        decrypted[i] = decrypted[i][shift[i]:] + decrypted[i][:shift[i]]
    return Image.fromarray(np.array(decrypted, dtype=np.uint8))

if __name__=='__main__':
    import os
    for image in os.listdir('images'):
        img = Image.open('images/'+image)
        enc = encrypt(img, 0.5, 3.8)
        enc.save('encrypted/logistic/'+image)