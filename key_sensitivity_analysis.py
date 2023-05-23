#Python equivalent of key_sensitivity_analysis.m

from PIL import Image
import cv2
import numpy as np
from PWLCM import encrypt as pwlcm, decrypt as dpwlcm
from LOGISTIC import encrypt as logistic, decrypt as dlogistic
from DLSCM2 import encrypt as dlscm, decrypt as ddlscm
from LSCML import encrypt as lscml, decrypt as dlscml

def compare(img1, img2):
    match_count = 0
    if img1.size != img2.size:
        return -1
    if img1.mode != img2.mode:
        return -1
    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            if img1.getpixel((i,j)) == img2.getpixel((i,j)):
                match_count+=1
    percent_match = (match_count/(img1.size[0]*img1.size[1]))*100
    return percent_match

def ksa_pwlcm(fname):
    img = Image.open(fname)
    img1 = pwlcm(img, 0.5, 0.8)
    img2 = pwlcm(img, 0.5, 0.9)
    match1 = compare(img1, img2)
    img3 = dpwlcm(img1, 0.5, 0.8)
    img4 = dpwlcm(img1, 0.6, 0.9)
    match2 = compare(img3, img4)
    print(fname + ': ', str(match1) + '%, ' + str(match2) + '%' ,sep='\t')
    
def ksa_logistic(fname):
    img = Image.open(fname)
    img1 = logistic(img, 0.5, 3.8)
    img2 = logistic(img, 0.5, 3.9)
    match1 = compare(img1, img2)
    img3 = dlogistic(img1, 0.5, 3.8)
    img4 = dlogistic(img1, 0.6, 3.9)
    match2 = compare(img3, img4)
    print(fname + ': ', str(match1) + '%, ' + str(match2) + '%' ,sep='\t')
    
def ksa_2dlscm(fname):
    img = Image.open(fname)
    #convert PIL image to cv2 image
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img1 = dlscm(img, key=None, q=[0.85,0.96,0.99,0.88],u=0.8,w=0.9)
    img2 = dlscm(img, key=None, q=[0.85,0.96,0.99,0.88],u=0.7,w=0.9)
    img3 = ddlscm(img1, key=None, q=[0.85,0.96,0.99,0.88],u=0.8,w=0.9)
    img4 = ddlscm(img1, key=None, q=[0.95,0.84,0.98,0.87],u=0.5,w=0.9)
    img1 = Image.fromarray(img1)
    img2 = Image.fromarray(img2)
    img3 = Image.fromarray(img3)
    img4 = Image.fromarray(img4)
    match1 = compare(img1, img2)
    match2 = compare(img3, img4)
    print(fname + ': ', str(match1) + '%, ' + str(match2) + '%' ,sep='\t')
    
def ksa_lscml(fname):
    img = Image.open(fname)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img1,sk1 = lscml(img, mkey=None, q=[0.85,0.96,0.99,0.88], u=0.8, w=0.9)
    img2,sk2 = lscml(img, mkey=None, q=[0.85,0.96,0.99,0.88], u=0.7, w=0.9)
    img3 = dlscml(img1, sk1, mkey=None, q=[0.85,0.96,0.99,0.88], u=0.8, w=0.9)
    img4 = dlscml(img1, sk2, mkey=None, q=[0.95,0.84,0.98,0.87], u=0.5, w=0.9)
    img1 = Image.fromarray(img1)
    img2 = Image.fromarray(img2)
    img3 = Image.fromarray(img3)
    img4 = Image.fromarray(img4)
    match1 = compare(img1, img2)
    match2 = compare(img1, img2)
    print(fname + ': ', str(match1) + '%, ' + str(match2) + '%' ,sep='\t')
    
if __name__=='__main__':
    import os
    print("PWLCM Key sensitivity: ")
    print("Name\t\tEnc\t\tDec")
    for img in os.listdir('images'):
        ksa_pwlcm('images/'+img)
    print("\nLOGISTIC Key sensitivity: ")
    print("Name\t\tEnc\t\tDec")
    for img in os.listdir('images'):
        ksa_logistic('images/'+img)
    print('\n2DLSCM Key sensitivity: ')
    print("Name\t\tEnc\t\tDec")
    for img in os.listdir('images'):
        ksa_2dlscm('images/'+img)
    print('\nLSCML Key sensitivity: ')
    print("Name\t\tEnc\t\tDec")
    for img in os.listdir('images'):
        ksa_lscml('images/'+img)