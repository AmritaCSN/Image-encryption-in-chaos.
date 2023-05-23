import numpy as np
from scipy.stats import entropy
from PIL import Image

def shannon_entropy(im):
    image = np.array(im)
    hist = np.histogram(image, bins=range(257))[0]
    hist = hist / np.sum(hist)
    return entropy(hist, base=2)


if __name__ == '__main__':
    import os
    import PWLCM
    import LOGISTIC
    import DLSCM2
    import LSCML
    import cv2
    print('IMAGE NAME\tORG ENTROPY\tPWLCM ENTROPY\tLOGISTIC ENTROPY\tDLSCM2 ENTROPY\tLSCML ENTROPY')
    for image in os.listdir('images'):
        img = Image.open('images/'+image)
        img_ = cv2.imread('images/'+image)
        enc1 = PWLCM.encrypt(img, 0.5, 0.8)
        enc2 = LOGISTIC.encrypt(img, 0.5, 3.8)
        enc3 = DLSCM2.encrypt(img_, b'hello')
        enc3 = Image.fromarray(enc3)
        enc4 = LSCML.encrypt(img_, b'hello')[0]
        enc4 = Image.fromarray(enc4)
        print(image, '\t', shannon_entropy(img), '\t', shannon_entropy(enc1), '\t', shannon_entropy(enc2), '\t', shannon_entropy(enc3), '\t', shannon_entropy(enc4))
