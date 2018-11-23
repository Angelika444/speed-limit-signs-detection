import numpy as np
import cv2




templates = [cv2.imread("signs/9.png", 0), cv2.imread("signs/8.png", 0), cv2.imread("signs/7.png", 0), cv2.imread("signs/6.png", 0), cv2.imread("signs/5.png", 0), cv2.imread("signs/4.png", 0), cv2.imread("signs/3.png", 0), cv2.imread("signs/2.png", 0), cv2.imread("signs/1.png", 0)]


def maxSpeed(signCutImage):

    ## PODSTAWOWY PARAMETR. IM MNIEJ WYM WIĘKSZA SZANSA ŻE WYKRYJE (ALE TEŻ WIĘKSZA SZANAS NA BŁĄD)
    threshold = 0.63
    #image 170x170 needed
    #znak 7
    image = signCutImage
    image = cv2.resize(image,(170,170))

    binary = (image > 120) * 255
    binary = np.uint8(binary)
    image = binary

    #cv2.imwrite('results/00start.png', image)

    if(image[12][85] == 0):
        image = image[12:158][12:158]
        image = cv2.resize(image,(170,170))
        



    #image = cv2.Laplacian(image, cv2.CV_64F)
    #cv2.imwrite('00start.png', image)

    #templates

    foundAtAll = 0
    foundElems = []
    templateNumber = 9
    for template in templates:
        w, h = template.shape[::-1]
        #template = cv2.Laplacian(template, cv2.CV_64F)
        #cv2.imwrite('00temp.png', template)


        #mach
        res = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc


        #dokładność
        
        loc = np.where( res >= threshold)

        foundPosOne = -1
        foundPosTwo = -1
        acctD = -1
        found = 0
        #wyniki
        #mean width of sign is 60px
        for pt in zip(*loc[::-1]):
            posX = pt[0]
            if(acctD == -1):
                ok = True
                for ff in foundElems:
                    if(abs(ff[1] - posX) < 40):
                        ok = False
                    
                if(ok):  
                    foundPosOne = posX
                    acctD = 0
                    cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 3)
                    print(posX)
                    foundElems.append([templateNumber, posX])
                    found = 1
            elif(acctD == 0):
                ok = True
                for ff in foundElems:   
                    if(abs(ff[1] - posX) < 40):
                        ok = False

                if(ok):
                    foundPosTwo = posX
                    acctD = 2
                    cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 3)
                    print(posX)
                    foundElems.append([templateNumber, posX])
                    found =2
                    continue

        foundAtAll += found
        if(foundAtAll >= 2):
            break
        
        templateNumber = templateNumber - 1


    if(foundAtAll == 0):
        return 'notFound'
    else:
        foundElems = sorted(foundElems,key=lambda l:l[1])
        filename = ''
        for elem in foundElems:
            filename = filename + str(elem[0])
        if(int(filename) <= 14):
            return (filename+'0')
        else:
            return 'notFound'

#
#
#
#
#
#
#print(time.time() - start)
#
#
#
#
#
#


start=[195000, 165000, 121000, 94000, 208000, 29000, 36000, 56000, 64000 , 72000, 79000, 86000, 234000, 106000, 118000, 4500, 158000]
stop=[200000, 170000, 124000, 100000, 210000, 30500, 38500, 58000, 68000, 74000, 81000, 88000, 237000, 112000, 121400, 6000, 159500]
name=['film4.mp4','film4.mp4','film4.mp4','film4.mp4','film2.mp4','film4.mp4','film4.mp4','film4.mp4','film4.mp4','film4.mp4','film4.mp4','film4.mp4','film2.mp4','film3.mp4','film3.mp4','film4.mp4','film1.mp4']

for jj in range(len(name)):
    speedLimit = 'nf'
    cap = cv2.VideoCapture(name[jj])
    cap.set(cv2.CAP_PROP_POS_MSEC, start[jj]) 
    koniec=stop[jj]
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    while (cap.get(cv2.CAP_PROP_POS_MSEC)<koniec):
        ret, img = cap.read()
          
        imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        sumS=0 #S z HSV
        sumV=0 #V z HSV
        sumRGB=0
        for i in range(int(imgHSV[0].size/3)):
            sumS+=imgHSV[0][i][1]
            sumV+=imgHSV[0][i][2]
               
        srS=int(0.8*sumS*3/imgHSV[0].size)
        srV=int(0.8*sumV*3/imgHSV[0].size)
        
        lower_red=np.array([0,min(40,srS),min(40,srV)])
        upper_red=np.array([10,255,255])
        mask1=cv2.inRange(imgHSV, lower_red,upper_red) #wybiera piksele, które są czerwone
        
        lower_red2=np.array([160,min(40,srS),min(40,srV)])
        upper_red2=np.array([179,255,255])
        mask2=cv2.inRange(imgHSV, lower_red2,upper_red2)#wybiera piksele, które są czerwone

        mask=cv2.add(mask1,mask2)
        imgRed = cv2.bitwise_and(img, img, mask = mask)
        
        imgGray=cv2.cvtColor(imgRed,cv2.COLOR_BGR2GRAY) #konwertuje zdjęcie z BGR do GrayScale

        r=5
        imgR = cv2.medianBlur(imgGray,r) #"rozmywa" zdjęcie, musi być w skali szarosci
        minradius=min(int(0.1*img.shape[0]),20)
        #alg. HoughCircles znajduje koło na zdjęciu, na wejciu img w skali szarosci, circles-np.array z inf. o pikselach
        circles = cv2.HoughCircles(imgR,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=minradius,maxRadius=90)
        
        srW=min(srV*(1+srS/255 -20),180)
        srB=max(50,srV*(1+srS/255))
            
        if circles is not None:
            while(r<60 and np.size(circles,1)>1): #"rozmywamy" obraz, aby było wykrywane tylko jedno  koło
            
                #circles = np.uint16(np.around(circles))#zaokragla war. do war. calkowitych
                #print(np.size(circles,1))
                if np.size(circles,1)<=10:
                    ii=0 #ktory wiersz do usuwania
                    for i in circles[0,:]:
                        count_White=0
                        count_Black=0
                        count_all=0
                        for j in img[int(i[1])-int(i[2]):int(i[1])+int(i[2]), int(i[0])-int(i[2]):int(i[0])+int(i[2])]:
                            for k in j:
                                count_all+=1
                                sr=(int(k[0])+int(k[1])+int(k[2]))/3
                                if sr>=srW:
                                    count_White+=1 #zliczamy biale piksele
                                elif sr<=srB:
                                    count_Black+=1 #zliczamy czarne piksele
                        if(count_all==0):
                            circles=np.delete(circles,ii,1)
                            ii-=1
                        elif(count_White/count_all<min(0.3,srS) or count_Black/count_all<0.1):
                            circles=np.delete(circles,ii,1)
                            #print(count_White/count_all,count_Black/count_all)
                            ii-=1
                        ii+=1
                   # print(np.size(circles,1), 'drugie')
                if np.size(circles,1)>1:               
                    r=r+2
                    imgR = cv2.medianBlur(imgGray,r)
                    circles = cv2.HoughCircles(imgR,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=minradius,maxRadius=90)
                    circles = np.uint16(np.around(circles))#zaokragla war. do war. calkowitych
                    #print(np.size(circles,1), 'trzecie', circles[0][0][2])
                while r<60 and np.size(circles,1)==0:
                    r=r+2
                    imgR = cv2.medianBlur(imgGray,r)
                    circles = cv2.HoughCircles(imgR,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=minradius,maxRadius=90)
                    while circles is None and r<60:
                        r+=2
                        imgR = cv2.medianBlur(imgGray,r)
                        circles = cv2.HoughCircles(imgR,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=40,minRadius=minradius,maxRadius=90)
                    #if circles is not None:
                     #   circles = np.uint16(np.around(circles))#zaokragla war. do war. calkowitych
            
        if circles is not None:
            circles = np.uint16(np.around(circles))#zaokragla war. do war. calkowitych
            #cv2.imshow('detected circles',img)
            x=int(circles[0][0][0])
            y=int(circles[0][0][1])
            r=int(circles[0][0][2])
            if x!=0 and y!=0 and r!=0:
                #okreslamy, na jakim obszarze jest znak i wycinamy go
                odx=max(x-r,0)
                dox=min(x+r,img.shape[1])
                ody=max(y-r,0)
                doy=min(y+r,img.shape[0])
                
                imgCrop = img[ody:doy, odx:dox].copy()
                #cv2.imshow("cropped", imgCrop)
                imgWhite=cv2.cvtColor(imgCrop,cv2.COLOR_BGR2GRAY)#konwertuje zdjęcie z BGR do GrayScale 
                speedLimitNew = maxSpeed(imgWhite)
                #speedLimitNew = 'notFound'
                if(speedLimitNew != 'notFound'):
                    speedLimit = ' ' + speedLimitNew + 'km/h'          
                    #cv2.imshow('gray image',imgWhite)
                    #cv2.waitKey(0)
                
                    for i in circles[0,:]:
                        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2) # rysuje koło
                
        
        if(speedLimit != 'nf'):
            cv2.putText(img = img, text = 'Ograniczenie predkosci!!!' + speedLimit, org = (int(frameWidth*0.1),int(frameHeight*0.8)), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 1.5, color = (0, 0,255))
        cv2.imshow('frame',img)
        if cv2.waitKey(1) == 27: 
            break # esc to quit

cap.release()
cv2.destroyAllWindows()