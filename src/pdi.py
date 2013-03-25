import cv2

img_file = 'data/larvas.jpg'

test = cv2.imread(img_file, 0)
(_, otsu) = cv2.threshold(test, 0.0, 255.0, \
                           cv2.THRESH_TOZERO_INV + cv2.THRESH_OTSU)

#cv2.imshow('otsu' , otsu)

(contornos, jerarquias) = cv2.findContours(otsu, mode=cv2.RETR_LIST \
                           , method=cv2.CHAIN_APPROX_NONE, offset=(0,0))

print 'cantidad de contornos: ' + str(len(contornos))
