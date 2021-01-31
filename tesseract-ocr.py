# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 17:03:19 2021

@author: gaura
"""

# import libraries
import pytesseract
from pytesseract import Output
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import re

# adding to path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# function to read image
def imgread(i):
    j = "{}".format(i) + ".jpg"
    k = cv2.imread(j)
    return k

# function to write image
def imgwrite(i, m):
    j = "Masked/{}".format(i) + ".jpg"
    cv2.imwrite(j, m)
    
# converting image to data using pytesseract
def imgtodata(i):
    j = pytesseract.image_to_data(i, output_type=Output.DICT)
    #print(j.keys())
    k = len(j['text'])
    return j, k

# printing some text beforehand
def sample(a, b):
    print(b)
    c = b//2
    for i in range(c, c + 5):
        print("Left: {}".format(a['left'][i]),
              "Top: {}".format(a['top'][i]),
              "Width: {}".format(a['width'][i]),
              "Height:{}".format(a['height'][i]),
              "Text:{}".format(a['text'][i]),
              "Conf:{}".format(a['conf'][i])
              )

# function to match patterns
def patterns(a, b, c):
    j = '^(0[1-9]|1[0-9]|2[0-9]|3[0-1])-(0[1-9]|1[0-2])-(20[0-9][0-9])' # date
    k = '^[A-Z0-9]{20}' # order id
    m = '^[A-Z0-9]{16}' # invoice no
    n = '^[A-Z0-9]{15}' # gstin
    o = '^[A-Z0-9]{10}' # pan
    #p = '(\d+)(\.)(\d+)\b' # price
    p = r'\d+\.\d{2}\b'
    q = []
    #q.append(1.00)
    for i in range(c):
        if re.match(j, b['text'][i]):
            j = b['text'][i]
        elif re.match(k, b['text'][i]):
            k = b['text'][i]
        elif re.match(m, b['text'][i]):
            m = b['text'][i]
        elif re.match(n, b['text'][i]):
            n = b['text'][i]
        elif re.match(o, b['text'][i]):
            o = b['text'][i]
        elif re.match(p, b['text'][i]):
            r = float(b['text'][i])
            #r = float(b['text'][i])
            q.append(r)
            #q.append(round(r, 2))
            #q.append("{0:.2f}".format(r))
            #q.append(float(b['text'][i]))
        else:
            continue
    return j, k, m, n, o, max(q)

# function to highlight text
def makebox(a, b, c):
    for i in range(c):
        (x, y, w, h) = b["left"][i], b["top"][i], b["width"][i], b["height"][i] 
        a = cv2.rectangle(a, (x, y), (x+w, y+h), (0, 255, 0), 1)
        a = cv2.putText(a, b['text'][i], (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 1)
    plt.imshow(a)
    return a

# for single image
#img = cv2.imread("1-crop.jpg")
#plt.imshow(img)

# main function
l = []
for i in range(1, 74):
    a = imgread(i)
    b, c = imgtodata(a)
    #d = sample(b, c)
    e = makebox(a, b, c)
    f = imgwrite(i, e)
    #q, r, s, t, u, v = patterns(a, b, c)
    l.append((patterns(a, b, c)))
    #w = {q, r, s, t, u, v}
    #x = {'Date' : q, 'Order Id' : r, 'Invoice No' : s, 'GSTIN' : t, 'PAN' : u, 'Price' : v}
    
alldata = pd.DataFrame(data = l, columns=('Date', 'Order Id', 'Invoice No', 'Gstin', 'Pan', 'Price'))
alldata.to_excel('alldata.xlsx')
