import cv2
import numpy as np
from skimage.feature import peak_local_max
from skimage.segmentation import clear_border
from scipy import ndimage

## ---------------------- READ IMAGE -------------------------------------------
img = cv2.imread('images/img_with_mask.jpg')

## ---------------------- DSP  -------------------------------------------------
img_b, img_g, img_r = cv2.split(img)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print('Load the image and convert it to grayscale:')

thresh_gray = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
thresh_blue = cv2.threshold(img_b, 120, 255, cv2.THRESH_BINARY)[1] # use without extraneous opencv stuff

kernel = np.ones((20, 20), np.uint8)
opening = cv2.morphologyEx(thresh_blue, cv2.MORPH_OPEN, kernel, iterations=10)

cnts = cv2.findContours(thresh_blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

superimposed_b_g = cv2.addWeighted(thresh_gray, 0.5, thresh_blue, 0.5, 0)

# print(len(thresh_blue[0])) # 1398 X 918
# for kernel_row_idx in range(len(thresh_blue) - np.shape(kernel)[0]):
#     for kernel_col_idx in range(len(thresh_blue[0] - np.shape(kernel)[1])):

print(cnts)

### how to get coordinates of blobs with opencv


cv2.imshow("Image with Centers", thresh_blue)
cv2.waitKey(0)

# thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# print('Apply a threshold to the grayscale image to separate the dots from the background:')

# kernel = np.ones((3, 3), np.uint8)
# opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
# print('Remove any small objects or holes in the thresholded image:')

# cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# print('Identify the contours of the dots:')

# # cnts = np.array(cnts)
# # cnts = clear_border(cnts)

# centers = []
# for c in cnts:
#     M = cv2.moments(c)
#     cX = int(M["m10"] / M["m00"])
#     cY = int(M["m01"] / M["m00"])
#     centers.append((cX, cY))
# print('Compute the center of each dot using the moments of the contour:')

# for center in centers:
#     cv2.circle(img, center, 5, (0, 0, 255), -1)
# cv2.imshow("Image with Centers", img)
# cv2.waitKey(0)
# print('Display the centers of the dots on the original image:')

