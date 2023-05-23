from PIL import Image
import math

def uaci(image1, image2):
    pixel1=image1.load()
    pixel2=image2.load()
    width,height=image1.size
    value=0.0
    try:
        for y in range(0,height):
            for x in range(0,width):
                value=(abs(pixel1[x,y][0]-pixel2[x,y][0])/255)+value
    except TypeError:
        for y in range(0,height):
            for x in range(0,width):
                value=(abs(pixel1[x,y]-pixel2[x,y])/255)+value
    value=(value/(width*height))*100
    return value

def rootmeansquareerror(image1, image2):
    pixel1 = image1.load()
    pixel2 = image2.load()
    width, height = image1.size
    value1 = 0.0
    value2=0.0
    value3=0.0
    try:
        for y in range(0,height):
            for x in range(0,width):
                value1=((pixel1[x,y][0]-pixel2[x,y][0])**2)+value1
                value2 = ((pixel1[x, y][1] - pixel2[x, y][1]) ** 2) + value2
                value3 = ((pixel1[x, y][2] - pixel2[x, y][2]) ** 2) + value3
    except TypeError:
        for y in range(0,height):
            for x in range(0,width):
                value1=((pixel1[x,y]-pixel2[x,y])**2)+value1
    value1=value1/(height*width)

    return (value1+value2+value3)/3
