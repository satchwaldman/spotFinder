from itertools import count
import cv2
import numpy as np

### ------------------------ CREATE MASK ---------------------------------------

# define a variable to keep track of the mouse button status
drawing = False

# define variables to keep track of the rectangle dimensions
ix, iy = -1, -1
fx, fy = -1, -1

# define a mouse callback function
def draw_rect(event, x, y, flags, param):
    global ix, iy, fx, fy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        fx, fy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            fx, fy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        fx, fy = x, y

# read in the image
img = cv2.imread('images/edited_dots_on_paper_1.jpg') # ENTER IMAGE FILEPATH

# create a window to display the image
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rect)

while True:
    # copy the original image
    img_copy = img.copy()

    # draw the rectangle on the copy image
    if ix != -1 and iy != -1 and fx != -1 and fy != -1:
        cv2.rectangle(img_copy, (ix, iy), (fx, fy), (0, 255, 0), 2)

    # display the image
    cv2.imshow('image', img_copy)

    # wait for a key press
    k = cv2.waitKey(1)

    # if the 'c' key is pressed, apply the mask to the image and exit the loop
    if k == ord('c'):
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (ix, iy), (fx, fy), (255, 255, 255), -1)
        masked_img = cv2.bitwise_and(img, img, mask=mask)
        break

    # if the 'q' key is pressed, exit the loop
    if k == ord('q'):
        break

masked_img[np.all(masked_img == (0,0,0), axis=-1)] = (255,255,255)

# cv2.imwrite("images/img_with_mask.jpg", masked_img)

### ----------------- MASKED IMAGE -> BLUE DATA BLACK AND WHITE IMAGE ----------

img_b, img_g, img_r = cv2.split(masked_img)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print('Load the image and convert it to grayscale:')

thresh_gray = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
thresh_blue = cv2.threshold(img_b, 120, 255, cv2.THRESH_BINARY)[1] # use without extraneous opencv stuff

### ------------------------ BLUE MASKED IMAGE -> CONTOURS ---------------------

# Read image in color (so we can draw in red)
# masked_img = cv2.imread("images/thresh_blue_with_mask.jpg")
# convert to gray and threshold to get a binary image
# gray = cv2.cvtColor(thresh_blue, cv2.COLOR_BGR2GRAY)
th, dst = cv2.threshold(thresh_blue, 20, 255, cv2.THRESH_BINARY)
# invert image
dst = cv2.bitwise_not(dst)
# find contours
countours,hierarchy=cv2.findContours(dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# draw contours
print('number of contours: ' + str(len(countours)))

### ------------------------ DISPLAY CONTOURS ----------------------------------
# for cnt in countours:
#         cv2.drawContours(masked_img,[cnt],0,(0,0,255),2)
#         cv2.imshow("Result",masked_img)
#         cv2.waitKey(2)
# # show image
# for cnt in countours:
#         cnt_img = cv2.drawContours(masked_img,[cnt],0,(0,0,255),2)
# cv2.imshow("Result",cnt_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

print(countours)

# TODO: 
# turn each contour into the center coordinates of the contour
# convert coordinates from pixels to physical dimensions
# append coordinates to list
# convert list into .xeo
