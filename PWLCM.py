from PIL import Image
import numpy as np

# Piecewise Linear Chaotic Map
def pwlcm(initial,p,r,c):
    t = initial
    res = []
    for i in range(r):
        res1=[]
        for j in range(c):
            if (t >= 0 and t < p):
                t = t/p
                res1.append(t)
            elif (t >= p and t<0.5):
                t = (t-p)/(0.5-p)
                res1.append(t)
            elif (t >= 0.5 and t<1):
                t = 1-t
                if (t >= 0 and t < p):
                    t = t/p
                    res1.append(t)
                elif (t >= p and t<0.5):
                    t = (t-p)/(0.5-p)
                    res1.append(t)
        res.append(res1)
    return res

def encrypt(img, initial, p):
    M,N = img.size
    vals = [[int(i*256) for i in j] for j in pwlcm(initial, p, M, N)]
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
    

def decrypt(img, initial, p):
    M,N = img.size
    vals = [[int(i*256) for i in j] for j in pwlcm(initial, p, M, N)]
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

if __name__ == '__main__':
    import os
    for image in os.listdir('images'):
        try:
            img = Image.open('images/'+image)
            enc = encrypt(img, 0.5, 0.8)
            enc.save('encrypted/pwlcm/'+image)
            print(f"Encrypted {image}")
        except:
            print(f"Error in {image}")