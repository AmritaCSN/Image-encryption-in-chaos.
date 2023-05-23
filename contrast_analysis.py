import numpy as np
from skimage.feature import graycomatrix, graycoprops
from skimage import io, color

def contrast_analysis(fname):
    # Load the image and convert it to grayscale
    image = io.imread(fname)
    try:
        image_gray = color.rgb2gray(image)
    except:
        image_gray = image
    image_gray_uint = (image_gray * 255).astype(np.uint8)

    # Calculate the GLCM matrix with distances of 1 pixel and angles of 0, 45, 90, and 135 degrees
    distances = [1]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    glcm = graycomatrix(image_gray_uint, distances=distances, angles=angles, levels=256, symmetric=True, normed=True)

    # Calculate the contrast of the image using the GLCM for each angle
    contrasts = [graycoprops(glcm, 'contrast')[0, 0] for angle in angles]

    # Calculate the average contrast from the four angles
    average_contrast = np.mean(contrasts)

    return average_contrast/255

if __name__=='__main__':
    import os
    print("ORIGINAL IMAGE CONTRAST: ")
    for i in os.listdir('images'):
        print(i + ': ' + str(contrast_analysis('images/'+i)))
    print("\nPWLCM: ")
    for i in os.listdir('images'):
        print(i + ': ' + str(contrast_analysis('encrypted/pwlcm/'+i)))
    print("\nLOGISTIC: ")
    for i in os.listdir('images'):
        print(i + ': ' + str(contrast_analysis('encrypted/logistic/'+i)))
    print("\n2DLSCM: ")
    for i in os.listdir('images'):
        print(i + ': ' + str(contrast_analysis('encrypted/2dlscm/'+i)))
    print("\nLSCML: ")
    for i in os.listdir('images'):
        print(i + ': ' + str(contrast_analysis('encrypted/lscml/'+i)))