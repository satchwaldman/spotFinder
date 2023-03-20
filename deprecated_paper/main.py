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
img_filename_no_ext = "edited_dots_on_paper_1"
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
### ------------------------ UNCOMMENT TO SEE FOR LONG TIME --------------------
## show image
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

### ----------- CONVERT COORDINATES FROM PIXELS TO PHYSICAL DIMENSIONS ---------
# Going to have trouble because this needs to be very precise
pixel_height = img_height / np.shape(img)[0]
pixel_width = img_width / np.shape(img)[1]

print("pixel height: " + str(pixel_height))
print("pixel width: " + str(pixel_width))

centers_coordinates = [(pixel_x * pixel_width, pixel_y * pixel_height) for (pixel_x, pixel_y) in centers]# append coordinates to list

# print("center coordinates list: \n" + str(centers_coordinates))
### ------------------------------ SORT PIXELS ---------------------------------

# def sort_pixels_by_row(pixels):
#     # Define a key function that returns the row and column values of a pixel tuple
#     def key_func(pixel):
#         row = pixel[1] // 10  # Compute the row index based on y-coordinate (assuming 10-pixel rows)
#         col = pixel[0]  # Column index is simply the x-coordinate
#         return row, col

#     # Sort the pixels using the key function
#     sorted_pixels = sorted(pixels, key=key_func)
    
#     return sorted_pixels

# centers_sorted = sort_pixels_by_row(centers)

######

# # sort center_coordinates based on each element's y-value 
# center_coords_sorted = sorted(centers_coordinates, key=lambda x: x[1])

# # now sort the x-values 
# curr_row_y = center_coords_sorted[0][1] # y-value that will set the intialize the row value 
# mat = [[]]
# row_y_delta = 8 # sets the number of pixels above and below that will be included in a row

# num_elems_up_to_curr_row = 0
# elem = 0
# row = 0
# while not len(mat) >= num_rows:
#     while curr_row_y <= row_y_delta:
#         mat[row].append(center_coords_sorted[elem])
#         elem += 1
#     row += 1




### --------------------------- GENERATE .XEO AS STRING ------------------------
xeo_string = ""
revision_number = 1.0 # update if making multiple .xeo files for the same image

xeo_string += "<!-- " + img_filename_no_ext + ".xeo -->"
xeo_string += "\n<!-- $Revision: " + str(revision_number) + " $ -->"
xeo_string += "\n<PlateType>"
xeo_string += "\n    <GlobalParameters PlateTypeName=\"" + img_filename + "\" ProbeType=\"MTP\""
xeo_string += "\n                      RowsNumber=\"32\" ChipNumber=\"1\" ChipsInRow=\"0\""
xeo_string += "\n                      X_ChipOffsetSize=\"0\" Y_ChipOffsetSize=\"0\""
xeo_string += "\n                      HasDirectLabels=\"false\" HasColRowLabels=\"false\""
xeo_string += "\n                      ProbeDiameterX=\"105.0282\" SampleDiameter=\"1.1423\" SamplePixelRadius=\"5\" ZoomFactor=\"1\""
xeo_string += "\n                      HasNearNeighbourCalibrants=\"false\""
xeo_string += "\n                      FirstCalibrant=\"X01Y01\" SecondCalibrant=\"X48Y01\" ThirdCalibrant=\"X24Y32\" />"
xeo_string += "\n    <MappingParameters mox=\"0\" moy=\"0\" sinphi=\"0.000000\" cosphi=\"1.000000\" alpha=\"100000\" beta=\"100000\" tansigma=\"0.000000\" />"
xeo_string += "\n    <PlateSpots PositionNumber=\"" + str(len(centers))+ "\">"

inc = 0
for (pixel_x, pixel_y) in centers_coordinates:
    xeo_string += "\n        <PlateSpot PositionIndex=\"" + str(inc) + "\" PositionName=\"X01Y01\" UnitCoord_X=\"" + str(pixel_x) + "\" UnitCoord_Y=\"" + str(pixel_y) + "\"/>"
    inc += 1

xeo_string += "\n    </PlateSpots>"
xeo_string += "\n</PlateType>"

### --------------------------- SAVE .XEO FILE IN xeo_files ---------------------------
xeo_filepath = "xeo_files/" + img_filename_no_ext + "_version_" + str(revision_number).replace(".", "_") + ".xeo"
# with open(xeo_filepath, "w") as f:
#     f.write(xeo_string)