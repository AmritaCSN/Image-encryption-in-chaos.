import os
import PWLCM
import LOGISTIC
import DLSCM2
import LSCML
from PIL import Image
import cv2
from time import time
from tabulate import tabulate as tb

def time_pwlcm(fname):
    img = Image.open(fname)
    start = time()
    c = PWLCM.encrypt(img,0.5,0.8)
    end = time()
    t0 = end - start
    start = time()
    d = PWLCM.decrypt(c,0.5,0.8)
    end = time()
    t1 = end - start
    return t0+t1

def time_logistic(fname):
    img = Image.open(fname)
    start = time()
    c = LOGISTIC.encrypt(img,0.5,3.8)
    end = time()
    t0 = end - start
    start = time()
    d = LOGISTIC.decrypt(c,0.5,3.8)
    end = time()
    t1 = end - start
    return t0+t1

def time_2dlscm(fname):
    img = cv2.imread(fname)
    start = time()
    c = DLSCM2.encrypt(img,b'hello')
    end = time()
    t0 = end - start
    start = time()
    d = DLSCM2.decrypt(c,b'hello')
    end = time()
    t1 = end - start
    return t0+t1

def time_lscml(fname):
    img = cv2.imread(fname)
    start = time()
    c,sk = LSCML.encrypt(img,b'hello')
    end = time()
    t0 = end - start
    start = time()
    d = LSCML.decrypt(c, sk, b'hello')
    end = time()
    t1 = end - start
    return t0+t1

# print("Image\tSize\tPWLCM(E)\tPWLCM(D)\tLOGISTIC(E)\tLOGISTIC(D)\tDLSCM2(E)\tDLSCM2(D)\tLSCML(E)\tLSCML(D)")
# for i in os.listdir('images'):
#     img = Image.open('images/'+i)
#     print(i + "\t" + 'x'.join(map(str,img.size)),end = '')
#     times = [time_pwlcm('images/'+i), time_logistic('images/'+i), time_2dlscm('images/'+i), time_lscml('images/'+i)]
#     for t in times:
#         print("\t" + str(t[0])[:4] + "\t" + str(t[1])[:4] ,end = '')
#     print()

output = [["Image", "Size", "PWLCM", "LOGISTIC", "2DLSCM", "LSCML"]]
l = os.listdir('images')
for i in range(len(l)):
    arr = [l[i]]
    img = Image.open('images/'+l[i])
    arr.append('x'.join(map(str,img.size)))
    times = [time_pwlcm('images/'+l[i]), time_logistic('images/'+l[i]), time_2dlscm('images/'+l[i]), time_lscml('images/'+l[i])]
    for t in times:
        arr.append(str(t)[:5])
    output.append(arr)
mytable = tb(output, headers='firstrow', tablefmt='fancy_grid')

print(mytable)   