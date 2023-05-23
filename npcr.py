from PIL import Image
import numpy as np

def rateofchange(height,width,pixel1,pixel2,matrix,i):
    for y in range(0,height):
        for x in range(0,width):
            #print(x,y)
            if pixel1[x,y] == pixel2[x,y]:
                matrix[x,y]=0
            else:
                matrix[x,y]=1
    return matrix

def sumofpixel(height,width,pixel1,pixel2,ematrix,i):
    matrix=rateofchange(height,width,pixel1,pixel2,ematrix,i)
    psum=0
    for y in range(0,height):
        for x in range(0,width):
            psum=matrix[x,y]+psum
    return psum

def npcr_(c1,c2):
    width, height = c1.size
    pixel1 = c1.load()
    pixel2 = c2.load()
    ematrix = np.empty([width, height])
    per=(((sumofpixel(height,width,pixel1,pixel2,ematrix,0)/(height*width))*100)+((sumofpixel(height,width,pixel1,pixel2,ematrix,1)/(height*width))*100)+((sumofpixel(height,width,pixel1,pixel2,ematrix,2)/(height*width))*100))/3
    return per

def npcr(c1,c2):
    width, height = c1.size
    s = 0
    pixel1 = c1.load()
    pixel2 = c2.load()
    try:
        for i in range(width):
            for j in range(height):
                for k in range(3):
                    if pixel1[i,j][k]!=pixel2[i,j][k]:
                        s+=1
        per = s/(width*height*3) * 100 
    except:
        for i in range(width):
            for j in range(height):
                if pixel1[i,j]!=pixel2[i,j]:
                    s+=1
        per = s/(width*height)*100
    return per

if __name__=='__main__':
    img1 = Image.open('images/couple.png')
    import LOGISTIC
    img2 = LOGISTIC.encrypt(img1, 0.5, 3.8)
    print(npcr(img1, img2))