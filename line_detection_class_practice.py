#!/usr/bin/env python
import numpy as np
import math
import cv2

filename = '01855_32_0.png'
org_img = cv2.imread(filename)
img = np.copy(org_img)  #create a copy of org_img
#cv2.imshow('org_img', org_img)

####################################
#1) Convert to gray scale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray_img', gray_img)

####################################
#2) Gaussian blur
blur_img = cv2.GaussianBlur(org_img, (5,5), 0)
#cv2.imshow('blur_img', blur_img)


####################################
#3) Canny edge detection (display the edge image)
edges = cv2.Canny(org_img, 150, 200)
#cv2.imshow('edges', edges)


#####################################
#Apply ROI
mask = np.zeros_like(edges)
vertices = [np.array([[0,480], [0, 350], [340, 200], [640, 350], [640, 480]], dtype = np.int32)]
cv2.fillPoly(mask, vertices, (255,255,255))
edges_ROI = cv2.bitwise_and(edges, mask)
#cv2.imshow('mask', mask)
#cv2.imshow('masked', masked)



####################################
#s4) Hough transform (display the line image)


edges_copy = np.copy(edges_ROI)
threshold = 10
minLineLength = 30
maxLineGap = 10
lines = cv2.HoughLinesP(
	edges_copy,
	1, # rho
	np.pi / 180, #theta
	threshold, #threshold
	np.array([]), #lines
	minLineLength, #min line length
	maxLineGap #max line gap
	)

# Use the following code to create a line image
line_img = np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8)
line_color=[0, 255, 0]
line_thickness=1
dot_color = [0, 255, 0]
dot_size = 3
for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), line_color, line_thickness)
            cv2.circle(line_img, (x1, y1), dot_size, dot_color, -1)
            cv2.circle(line_img, (x2, y2), dot_size, dot_color, -1)
#cv2.imshow('lines', line_img)


####################################
#5) Overlay (i.e., blend) the line image with the original image
overlay = cv2.addWeighted(org_img, 0.8, line_img, 1.0, 0.0)
cv2.imshow('overlay', overlay)

'''
####################################
slopes = []
lines_rev = []
for line in lines:
	for x1, y1, x1, y2 in line:		
		s = 0
		if x2-x1 != 0:
			s = float((y2-y1)/(x2-x1))			
		else:
			slopes.extend([9999])
		if s < 1:# & s > 0.3:
				lines_rev = line
		

for line in lines_rev:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), line_color, line_thickness)
            cv2.circle(line_img, (x1, y1), dot_size, dot_color, -1)
            cv2.circle(line_img, (x2, y2), dot_size, dot_color, -1)

#for slope in slopes:
#	if slope < 1.0 && slope > 0.3:

#slops_abs = abs(slopes)

'''


cv2.waitKey(0)  #press any key to quit
cv2.destroyAllWindows()