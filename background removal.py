# Importar cv2 para capturar el video.
import cv2
import time
import numpy as np

# Establecer el índice de cámara como 0.
vid = cv2.VideoCapture(0)

# Establecer el ancho y altura del cuadro como 640 X 480.
vid.set(3 , 640)
vid.set(4 , 480)

fourcc=cv2.VideoWriter_fourcc(*'XVID')
outputfile=cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
time.sleep(2)
bg=0
for i in range(60):
   ret,bg=vid.read()
bg=np.flip(bg,axis=1)

# Cargar la imagen de la montaña.
mountain = cv2.imread('mount everest.jpg')

while True:

 #Separa el video entre imagnes
    ret, frame=vid.read()
    if not ret:
       break
    frame=np.flip(frame, axis=1)
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerred=np.array([0, 120, 50])
    upperred=np.array([10, 255, 255])
    mask1=cv2.inRange(hsv, lowerred, upperred)

#mask1 guarda color rojo, mask2 se guarda el no color rojo

    lowerred=np.array([170, 120, 70])
    upperred=np.array([180, 255, 255])
    mask2=cv2.inRange(hsv, lowerred, upperred)
    mask1=mask1+mask2
    cv2.imshow("mascara1",mask1)
    #Eliminarruido de la imagen
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE, np.ones((3,3), np.uint8))


    #Segmentación del rojo
    #guarda el no rojo
    mask2=cv2.bitwise_not(mask1)
    rest1=cv2.bitwise_and(frame, frame, mask=mask2)
    rest2=cv2.bitwise_and(bg,bg,mask=mask1)
 
    #generar la imagen
    finaloutput=cv2.addWeighted(rest1,1,rest2, 1,0)
    outputfile.write(finaloutput)


    cv2.imshow("Finalout", finaloutput)
    
    if cv2.waitKey(25)==32:
     break


# Soltar la cámara y cerrar todas las ventanas abiertas.
camera.release()
cv2.destroyAllWindows()
