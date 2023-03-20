from itertools import count
import cv2
import numpy as np
from sklearn.metrics import zero_one_loss

### ---------------------------- OVERVIEW --------------------------------------

# turn each contour into the center coordinates of the contour
# add a way to remove or add more dots
# convert coordinates from pixels to physical dimensions
# append coordinates to list
# convert list into .xeo

### ------------------------ ASK USER FOR IMAGE DIMENSIONS ---------------------
img_height_str = input("Please enter your height in centimeters: ")
img_width_str = input("Please enter your width in centimeters: ")

img_height = float(img_height_str)
img_width = float(img_width_str)

num_rows = input("Please enter the number of rows: ")

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
img_filename_no_ext = "trial_1_second_edit"
img_filename = img_filename_no_ext + ".jpg" # ENTER IMAGE FILEPATH
folder = 'images'
filepath = folder + '/' + img_filename
img = cv2.imread(filepath) 

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

### ------------------------ DISPLAY CONTOUR POPULATION ------------------------
# for cnt in countours:
#         cv2.drawContours(masked_img,[cnt],0,(0,0,255),2)
#         cv2.imshow("Result",masked_img)
#         cv2.waitKey(2)
# ## ------------------------ UNCOMMENT TO SEE FOR LONG TIME --------------------
# # show image
# for cnt in countours:
#         cnt_img = cv2.drawContours(masked_img,[cnt],0,(0,0,255),2)
# cv2.imshow("Result",cnt_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# print(countours)

# flat_contours = np.array(countours).reshape(-1, 2)
# split_contours = np.split(flat_contours, len(countours[0]), axis=0)

### ------------------------ COMPUTE CENTERS -----------------------------------

centers = []

for contour in countours:
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centers.append((cX, cY))

# print(centers)

img_centers = img.copy() #np.zeros(np.shape(img))
for center in centers:
    x, y = center
    img_centers[y][x] = [0, 0, 255]

print(centers)

# cv2.imshow("Image with Centers",img_centers)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite("images/img_with_centers.jpg", img_centers)

### ------------------------ ADD MISSED CENTERS AND DELETE ERRONEOUS ONES----------------------------------

def on_mouse_click(event, x, y, flags, param):
    global centers, img, img_centers
    
    if event == cv2.EVENT_LBUTTONDOWN: # add a new point
        centers.append((x, y))
        # draw a pixel at the clicked position
        cv2.line(img_centers, (x, y), (x, y), (0, 0, 255), 1)
    elif event == cv2.EVENT_RBUTTONDOWN: # remove a point
        for i in range(len(centers)):
            center = centers[i]
            if abs(center[0] - x) < 5 and abs(center[1] - y) < 5:
                del centers[i]
                break
        # redraw all the points
        img_centers = img.copy() # clear the image
        for center in centers:
            cv2.line(img_centers, center, center, (0, 0, 255), 1)

cv2.namedWindow('image')
cv2.setMouseCallback('image', on_mouse_click)

while True:
    cv2.imshow('image', img_centers)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        # cv2.imwrite("images/img_with_centers_added.jpg", img)
        print("number of centers after additions: " + str(len(centers))) # could be a bug -- number of centers less than number of contours
        break

cv2.destroyAllWindows()

### ----------------------- SAVE CENTERS FOR LATER USE -------------------------
# this allows us to tweak the row_y_delta until it is optimal

with open("meta_data/centers.txt", "w") as f:
    f.write(str(centers))

with open("meta_data/height.txt", "w") as f:
    f.write(str(img_height))

with open("meta_data/width.txt", "w") as f:
    f.write(str(img_width))

with open("meta_data/rows.txt", "w") as f:
    f.write(str(num_rows))

