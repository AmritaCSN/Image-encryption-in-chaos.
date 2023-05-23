import cv2
import numpy as np
import math
import time
from skimage.measure import shannon_entropy
from hashlib import sha256
import matplotlib.pyplot as plt

def encrypt(img, mkey=None, q = None, u = None, w = None):
    rows, cols, ch = img.shape
    x=[]
    y=[]
    z=[]
    if mkey!=None:
        mkey = sha256(mkey).digest()[:12]
        q = [mkey[0]/mkey[1], mkey[2]/mkey[3], mkey[4]/mkey[5], mkey[6]/mkey[7]]
        q = [1.0/_ if _>1.0 else _ for _ in q]
        u=float(mkey[8]/mkey[9])
        if u>1.0:
            u=1.0/u
        w=float(mkey[10]/mkey[11])
        if w>1.0:
            w=1.0/w
    else:
        if q:
            q=[0.85,0.96,0.99,0.88]
        if u:
            u = float(0.8)
        if w:
            w = float(0.9)
    x.append(u)
    y.append(w)
    for count in range(0,4):
        r=q[count]
        ctr = 0
        for i in range(0,rows):
            for j in range(0,cols):
                x.append(math.sin(math.pi*(4*r*x[ctr]*(1-x[ctr])+(1-r)*math.sin(math.pi*y[ctr]))))
                y.append(math.sin(math.pi*(4*r*y[ctr]*(1-y[ctr])+(1-r)*math.sin(math.pi*x[ctr+1]))))
#				z.append(x[0]*y[0])
                ctr=ctr+1
    A=np.reshape(x[0:ctr],[rows,cols])
    F=np.reshape(y[0:ctr],[rows,cols])
#	A=np.reshape(z[0:ctr],[rows,cols])
#	F=np.reshape(z[0:ctr],[rows,cols])
    x.insert(0,x[ctr])
    y.insert(0,y[ctr])
    O=np.argsort(A,axis=0)
    t=np.zeros((rows,cols))
#	for i in range(0,rows):
#		g=[]
#		tmp=[]
#		for k in range(0,cols):
#			g.append(A[(O[i][k]),k])
#			tmp.append((O[i][k]))
#		v=np.argsort(g)
#		for f in range(0,cols):
#			a=tmp[v[f]]
#			b=v[f]
#			t[O[i][f]][f]=img[a][b][0]
    po = 8
    key =256
    c=np.zeros((rows,cols))
    c2 = np.zeros((rows,cols))

    for a in range(rows):
        for b in range(cols):
            t[a][b] = img[a][b][0]

    # Pixel Scrambling and Confusion

    # Pixel Scrambling Key Generation and Shuffling
    scramble_key = np.zeros((rows,cols))
    index_matrix = np.arange(rows*cols)
    np.random.shuffle(index_matrix)
    
    scramble_key = index_matrix.reshape([rows,cols])
    
    flatten_t = np.ndarray.flatten(t)
    for i in range(rows):
        for j in range(cols):
            c2[i][j] = flatten_t[scramble_key[i][j]]

    for a in range(rows):
        for b in range(cols):
            t[a][b] = c2[a][b]

    # Diffusion

    for i in range(0,rows):
        if ( i == 0):
            c[i,:] = ((t[0,:]+t[rows-1,:]+t[rows-2,:]+F[:,i]*pow(2,po))%key)
        elif ( i == 1):
            c[i,:] = ((t[1,:]+c[0,:]+t[rows-1,:]+F[:,i]*pow(2,po))%key)
        else:
            c[i,:] = ((t[i,:]+c[i-1,:]+c[i-2,:]+F[:,i]*pow(2,po))%key)

    for i in range(0,cols):
        if ( i == 0):
            c[:,i] = ((t[:,0]+t[:,cols-1]+t[:,cols-2]+F[:,i]*pow(2,po))%key)
        elif ( i == 1):
            c[:,i] = ((t[:,1]+c[:,0]+t[:,cols-1]+F[:,i]*pow(2,po))%key)
        else:
            c[:,i] = ((t[:,i]+c[:,i-1]+c[:,i-2]+F[:,i]*pow(2,po))%key)
    return c, scramble_key

def decrypt(img, scramble_key, mkey=None, q=None,u=None,w=None):
    rows, cols = img.shape
    x=[]
    y=[]
    z=[]
    if mkey!=None:
        key = sha256(mkey).digest()[:12]
        q = [key[0]/key[1], key[2]/key[3], key[4]/key[5], key[6]/key[7]]
        q = [1.0/_ if _>1.0 else _ for _ in q]
        u=float(key[8]/key[9])
        if u>1.0:
            u=1.0/u
        w=float(key[10]/key[11])
        if w>1.0:
            w=1.0/w
    else:
        if q:
            q=[0.85,0.96,0.99,0.88]
        if u:
            u = float(0.8)
        if w:
            w = float(0.9)
    x.append(u)
    y.append(w)
    for count in range(0,4):
        r=q[count]
        ctr = 0
        for i in range(0,rows):
            for j in range(0,cols):
                x.append(math.sin(math.pi*(4*r*x[ctr]*(1-x[ctr])+(1-r)*math.sin(math.pi*y[ctr]))))
                y.append(math.sin(math.pi*(4*r*y[ctr]*(1-y[ctr])+(1-r)*math.sin(math.pi*x[ctr+1]))))
                ctr=ctr+1
    A=np.reshape(x[0:ctr],[rows,cols])
    F=np.reshape(y[0:ctr],[rows,cols])
    x.insert(0,x[ctr])
    y.insert(0,y[ctr])
    O=np.argsort(A,axis=0)
    po = 8
    key =256
    d=np.zeros((rows,cols))
    c = img
    for i in range(0,rows):
        if (i>1):
            d[i,:] = ((c[i,:]-c[i-1,:]-c[i-2,:]-F[:,i]*pow(2,po))%key)
        elif (i==1):
            d[i,:] = ((c[1,:]-c[0,:]-c[rows-1,:]-F[:,i]*pow(2,po))%key)
        elif (i==0):
            d[i,:] = ((c[0,:]-c[rows-1,:]-c[rows-2,:]-F[:,i]*pow(2,po))%key)
    for i in range(0,cols):
        if (i>1):
            d[:,i] = ((c[:,i]-c[:,i-1]-c[:,i-2]-F[:,i]*pow(2,po))%key)
        elif (i==1):
            d[:,i] = ((c[:,1]-c[:,0]-c[:,cols-1]-F[:,i]*pow(2,po))%key)
        elif (i==0):
            d[:,i] = ((c[:,0]-c[:,cols-1]-c[:,cols-2]-F[:,i]*pow(2,po))%key)
    d2 = np.zeros(rows*cols)
    for i in range(rows):
        for j in range(cols):
            d2[scramble_key[i][j]] = d[i][j] 

    d = d2.reshape([rows,cols])
    return d

if __name__=='__main__':
    import os
    for i in os.listdir('images'):
        img = cv2.imread('images/'+i)
        enc = encrypt(img, b'password')
        cv2.imwrite('encrypted/lscml/'+i, enc[0])
            
