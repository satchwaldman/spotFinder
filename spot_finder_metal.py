import numpy as np
import cv2

### ------------------------ ASK USER FOR IMAGE DIMENSIONS ---------------------
img_height = 7.8
img_width = 12.0

num_rows_str = input("Please enter the number of rows: ")
num_columns_str = input("Please enter the number of columns: ")

num_rows_int = int(num_rows_str)
num_columns_int = int(num_columns_str)

num_rows = float(num_rows_int)
num_columns = float(num_columns_int)

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

initial_x = 0
initial_y = 0
final_x = 0
final_y = 0

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
        initial_x = ix
        initial_y = iy
        final_x = fx
        final_y = fy
        break

    # if the 'q' key is pressed, exit the loop
    if k == ord('q'):
        break

masked_img[np.all(masked_img == (0,0,0), axis=-1)] = (255,255,255)

### ------------------------- GENERATE DOTS ------------------------------------

x_vals = np.linspace(int(initial_x), int(final_x), num_columns_int)
y_vals = np.linspace(int(initial_y), int(final_y), num_rows_int)

dots_matrix_floats = np.zeros((num_rows_int, num_columns_int, 2))
dots_matrix = [[[int(num) for num in sublist] for sublist in nested_list] for nested_list in dots_matrix_floats]

for row_idx in range(len(y_vals)):
    for col_idx in range(len(x_vals)):
        dots_matrix[row_idx][col_idx] = [x_vals[col_idx], y_vals[row_idx]]


### ------------------------ DISPLAY DOTS OVER IMAGE ---------------------------

# print(dots_matrix)

# print('\n\n\n')

# print(masked_img)

# img_with_dots = masked_img.copy()

# print('\n\n\n')

# print(img_with_dots)

# print(np.shape(img_with_dots))

# for row in dots_matrix:
#     for center in row:
#         pixel_x, pixel_y = center[0], center[1]
#         img_with_dots[int(pixel_y)][int(pixel_x)] = [0, 0, 255]

# img_with_dots[initial_y, initial_x] = [0, 255, 0]
# img_with_dots[initial_y, final_x] = [0, 255, 0]
# img_with_dots[final_y, initial_x] = [0, 255, 0]
# img_with_dots[final_y, final_x] = [0, 255, 0]

# cv2.imshow("Image", img_with_dots)
# cv2.waitKey(0)

### -------------------------- MANUALLY ADJUST CENTERS ------------------------------------

# Define the 2D matrix of coordinates

dots_matrix_np = np.array(dots_matrix)
coords_2d_flat = dots_matrix_np.reshape(-1, 2)

coordinates = np.array([[int(x), int(y)] for [y, x] in coords_2d_flat])

# Define the color of the selected pixel
selected_color = (0, 255, 0)  # Green

# Define the function to display the image
def display_image():
    img_temp = img.copy()
    for coord in coordinates:
        img_temp[coord[0], coord[1]] = (0, 0, 255)  # Red
    cv2.imshow('image', img_temp)

# Define the mouse callback function
def mouse_callback(event, x, y, flags, param):
    global selected_index
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_coord = [y, x]  # Reverse the order of x, y
        print('Selected pixel:', selected_coord)
        # Map the pixel coordinates to the corresponding index in the 2D matrix
        selected_index = np.argmin(np.sum(np.abs(coordinates - selected_coord), axis=1))
        print('Selected index:', selected_index)
        # Display the selected pixel
        img_temp = img.copy()#np.zeros((918, 1398, 3), np.uint8)  # Create a blank image
        img_temp[coordinates[selected_index][0], coordinates[selected_index][1]] = selected_color
        cv2.imshow('image', img_temp)

# Define the keyboard callback function
def keyboard_callback(key):
    global selected_index
    global coordinates

    # Move the selected pixel based on the arrow key pressed
    if key == ord('w'):
        coordinates[selected_index][0] -= 1  # Move up
    elif key == ord('s'):
        coordinates[selected_index][0] += 1  # Move down
    elif key == ord('a'):
        coordinates[selected_index][1] -= 1  # Move left
    elif key == ord('d'):
        coordinates[selected_index][1] += 1  # Move right

    # Update the image to reflect the new position of the selected pixel
    img_temp = img.copy()
    for coord in coordinates:
        img_temp[coord[0], coord[1]] = (0, 0, 255)  # Red
    img_temp[coordinates[selected_index][0], coordinates[selected_index][1]] = selected_color
    cv2.imshow('image', img_temp)

# Display the image
display_image()

# Set up the mouse callback function
cv2.setMouseCallback('image', mouse_callback)

# Set up the keyboard callback function
while True:
    key = cv2.waitKey(0)
    if key == 27:  # Esc key
        break
    keyboard_callback(key)

# Close all windows
cv2.destroyAllWindows()

### --------------------- DISPLAY RESULTS FOR 5 SEC ----------------------------

# img_result = img.copy()
# for coord in coordinates:
#     img_result[coord[0], coord[1]] = (0, 0, 255)  # Red

# cv2.imshow("result", img_result)
# cv2.waitKey(5000)

### --------------------- RESULTS MATRIX (1,1) CALIBRATION ---------------------

# y: top down -> pos - neg
# x: left right -> neg - pos

coordinates_scaled = []
for [y, x] in coordinates:
    x_new = 2 * ((x - len(img[0]) / 2) / len(img[0]))
    y_new = 2 * ((len(img) / 2 - y) / len(img))
    coordinates_scaled.append([x_new, y_new])

result_matrix = np.zeros((num_rows_int, num_columns_int, 2))
start_idx = 0
for row in range(num_rows_int):
    result_matrix[row] = coordinates_scaled[start_idx: start_idx + num_columns_int]
    start_idx += num_columns_int

### --------------------------- GENERATE .XEO AS STRING ------------------------
xeo_string = ""
revision_number = input("Please enter revision number AS A DECIMAL (for example, 1.0): ") # update if making multiple .xeo files for the same image

xeo_string += "<!-- " + img_filename_no_ext + ".xeo -->"
xeo_string += "\n<!-- $Revision: " + str(revision_number) + " $ -->"
xeo_string += "\n<PlateType>"
xeo_string += "\n    <GlobalParameters PlateTypeName=\"" + img_filename + "\" ProbeType=\"MTP\""
xeo_string += "\n                      RowsNumber=\"32\" ChipNumber=\"1\" ChipsInRow=\"0\""
xeo_string += "\n                      X_ChipOffsetSize=\"0\" Y_ChipOffsetSize=\"0\""
xeo_string += "\n                      HasDirectLabels=\"false\" HasColRowLabels=\"false\""
xeo_string += "\n                      ProbeDiameterX=\"105.0282\" SampleDiameter=\"1.1423\" SamplePixelRadius=\"5\" ZoomFactor=\"1\""
xeo_string += "\n                      HasNearNeighbourCalibrants=\"false\""
xeo_string += "\n                      FirstCalibrant=\"X01Y01\" SecondCalibrant=\"X" + str(num_columns_int) + "Y1\" ThirdCalibrant=\"X" + str(int(np.floor(num_columns_int / 2))) + "Y" + str(num_rows_int) + "\" />"
xeo_string += "\n    <MappingParameters mox=\"0\" moy=\"0\" sinphi=\"0.000000\" cosphi=\"1.000000\" alpha=\"100000\" beta=\"100000\" tansigma=\"0.000000\" />"
xeo_string += "\n    <PlateSpots PositionNumber=\"" + str(len(coordinates))+ "\">"

row_idx = 1
inc = 0
for row in result_matrix:
    col_idx = 1
    for center in row:
        pixel_x = center[0]
        pixel_y = center[1]
        xeo_string += "\n        <PlateSpot PositionIndex=\"" + str(inc) + "\" PositionName=\"X" + str(col_idx) + "Y" + str(row_idx) + "\" UnitCoord_X=\"" + str(pixel_x) + "\" UnitCoord_Y=\"" + str(pixel_y) + "\"/>"
        inc += 1
        col_idx += 1
    row_idx += 1
    

xeo_string += "\n    </PlateSpots>"
xeo_string += "\n</PlateType>"

### --------------------------- SAVE .XEO FILE IN xeo_files ---------------------------
xeo_filepath = "xeo_files/" + img_filename_no_ext + "_version_" + str(revision_number).replace(".", "_") + ".xeo"
with open(xeo_filepath, "w") as f:
    f.write(xeo_string)


