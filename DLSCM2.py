import cv2
from skimage.measure import shannon_entropy
from hashlib import sha256
import numpy as np
import math 
import time

def encrypt(img, key=None, q=None, u=None, w=None):
    try:
       rows,cols,ch=img.shape
    except:
       rows,cols=img.shape
    x=[]
    y=[]
    z=[]
    if key:
        key = sha256(key).digest()[:12]
        q = [key[0]/key[1], key[2]/key[3], key[4]/key[5], key[6]/key[7]]
        u=float(key[8]/key[9])
        w=float(key[10]/key[11])
    else:
        if not q:
            q=[0.85,0.96,0.99,0.88]
        if not u:
            u = float(0.8)
        if not w:
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
    t=np.zeros((rows,cols))
    po = 8
    key =256
    c=np.zeros((rows,cols))

    for a in range(rows):
        for b in range(cols):
            t[a][b] = img[a][b][0]

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

    return c

def decrypt(img, key=None, q=None, u=None, w=None):
    rows,cols=img.shape
    x=[]
    y=[]
    z=[]
    if key:
        key = sha256(key).digest()[:12]
        q = [key[0]/key[1], key[2]/key[3], key[4]/key[5], key[6]/key[7]]
        u=float(key[8]/key[9])
        w=float(key[10]/key[11])
    else:
        if not q:
            q=[0.85,0.96,0.99,0.88]
        if not u:
            u = float(0.8)
        if not w:
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
            
    return d

if __name__=='__main__':
    import os
    for i in os.listdir('images'):
        img = cv2.imread('images/'+i)
        enc = encrypt(img, b'password')
        cv2.imwrite('encrypted/2dlscm/'+i, enc)