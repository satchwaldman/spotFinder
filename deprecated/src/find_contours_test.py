from itertools import count
import cv2
import numpy as np
# Read image in color (so we can draw in red)
img = cv2.imread("images/thresh_blue_with_mask.jpg")
# convert to gray and threshold to get a binary image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
th, dst = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
# invert image
dst = cv2.bitwise_not(dst)
# find contours
countours,hierarchy=cv2.findContours(dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# draw contours
print(len(countours))
for cnt in countours:
        cv2.drawContours(img,[cnt],0,(0,0,255),2)
        cv2.imshow("Result",img)
        cv2.waitKey(100)
# show image
cv2.imshow("Result",img)
cv2.waitKey(0)
cv2.destroyAllWindows()