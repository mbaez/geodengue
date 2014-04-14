#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2


def cantidad_contornos():
    img_file = 'data/file.jpeg'
    test = cv2.imread(img_file, 0)
    (_, otsu) = cv2.threshold(test, 0.0, 255.0,
                              cv2.THRESH_TOZERO_INV + cv2.THRESH_OTSU)

    (contornos, jerarquias) = cv2.findContours(otsu,
                                               mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE, offset=(0, 0))

    print 'cantidad de contornos: ' + str(len(contornos))
    return len(contornos)

if __name__ == "__main__":
    img_file = 'data/file.jpeg'
    test = cv.imread(img_file, 0)
    (_, otsu) = cv2.threshold(test, 0.0, 255.0,
                              cv2.THRESH_TOZERO_INV + cv2.THRESH_OTSU)

    (contornos, jerarquias) = cv2.findContours(otsu,
                                               mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE, offset=(0, 0))

    print 'cantidad de contornos: ' + str(len(contornos))
