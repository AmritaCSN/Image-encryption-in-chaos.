import os
import PWLCM
import LOGISTIC
import DLSCM2
import LSCML
import npcr
import uaci
import random
from PIL import Image
import cv2

def flip_random_pixel(img):
    M, N = img.size
    x, y = random.randint(0, M-1), random.randint(0, N-1)
    pixel = list(img.getpixel((x, y)))
    i = random.randint(0, 2)
    pixel[i] ^= 1
    pixel = tuple(pixel)
    img.putpixel((x, y), pixel)
    return img

def get_npcr_PWLCM():
    for image in os.listdir('images'):
        img = Image.open('images/'+image)
        enc = PWLCM.encrypt(img, 0.5, 0.8)
        print(image + ": ", npcr.npcr(img, enc))

def get_npcr_LOGISTIC():
    for image in os.listdir('images'):
        img = Image.open('images/'+image)
        enc = LOGISTIC.encrypt(img, 0.5, 3.8)
        print(image + ": ", npcr.npcr(img, enc))

def get_npcr_DLSCM2():
    for image in os.listdir('images'):
        img = cv2.imread('images/'+image)
        enc = cv2.imread('encrypted/2dlscm/'+image)
        img,enc = Image.fromarray(img), Image.fromarray(enc)
        print(image + ": ", npcr.npcr(img, enc))

def get_npcr_LSCML():
    for image in os.listdir('images'):
        img = cv2.imread('images/'+image)
        enc = cv2.imread('encrypted/lscml/'+image)
        img,enc = Image.fromarray(img), Image.fromarray(enc)
        print(image + ": ", npcr.npcr(img, enc))
        
def get_uaci_PWLCM():
    for image in os.listdir('images'):
        img = Image.open('images/'+image)
        enc = PWLCM.encrypt(img, 0.5, 0.8)
        print(image + ": ", uaci.uaci(img, enc))

def get_uaci_LOGISTIC():
    for image in os.listdir('images'):
        img = Image.open('images/'+image)
        enc = LOGISTIC.encrypt(img, 0.5, 3.8)
        print(image + ": ", uaci.uaci(img, enc))


def get_uaci_DLSCM2():
    for image in os.listdir('images'):
        img = cv2.imread('images/'+image)
        enc = cv2.imread('encrypted/2dlscm/'+image)
        img,enc = Image.fromarray(img), Image.fromarray(enc)
        print(image + ": ", uaci.uaci(img, enc))

def get_uaci_LSCML():
    for image in os.listdir('images'):
        img = cv2.imread('images/'+image)
        enc = cv2.imread('encrypted/lscml/'+image)
        img,enc = Image.fromarray(img), Image.fromarray(enc)
        print(image + ": ", uaci.uaci(img, enc))
        

if __name__=='__main__':
    print("PWLCM NPCR:")
    get_npcr_PWLCM()
    print("\nLOGISTIC NPCR:")
    get_npcr_LOGISTIC()
    print("\nPWLCM UACI:")
    get_uaci_PWLCM()
    print("\nLOGISTIC UACI:")
    get_uaci_LOGISTIC()
    print("\nDLSCM2 NPCR:")
    get_npcr_DLSCM2()
    print("\nDLSCM2 UACI:")
    get_uaci_DLSCM2()
    print("\nLSCML UACI:")
    get_uaci_LSCML()
    print("\nLSCML NPCR:")
    get_npcr_LSCML()