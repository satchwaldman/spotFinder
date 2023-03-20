import numpy as np
import cv2
import ast

### --------------- SET PARAMETERS AND READ IMAGE AND CENTERS ------------------

with open('height.txt', 'r') as file:
    img_height = float(file.read())

with open('width.txt', 'r') as file:
    img_width = float(file.read())

with open('rows.txt', 'r') as file:
    num_rows = float(file.read())

# read in the image
img_filename_no_ext = "plate_with_paper" # ENTER IMAGE FILEPATH
img_filename = img_filename_no_ext + ".jpg" 
folder = 'images'
filepath = folder + '/' + img_filename
img = cv2.imread(filepath) 

# read in centers 
with open('centers.txt', 'r') as file:
    centers_str = file.read()

centers = ast.literal_eval(centers_str)

### ------------------------------ SORT PIXELS ---------------------------------

centers_list = [list(t) for t in centers]

centers_sorted = sorted(centers_list, key=lambda x: x[1])

# print(len(center_coords_sorted))

# now sort the x-values 
curr_row_y = centers_sorted[0][1] # y-value that will set the intialize the row value 
mat = []
row_y_delta = 11 # sets the number of pixels above and below that will be included in a row

# num_elems_up_to_curr_row = 0
elem = 0
row = 0
num_rows = 8
print('entering loop')
while not len(mat) >= num_rows:
    mat.append([])
    while np.abs(centers_sorted[elem][1] - curr_row_y) <= row_y_delta:
        mat[row].append(centers_sorted[elem])
        elem += 1
        print("elem: " + str(elem))
        print("current delta: " + str(curr_row_y - centers_sorted[elem][1]))
    row += 1
    curr_row_y = centers_sorted[elem][1]
    print("row: " + str(row))

# print(mat)

sorted_mat = [sorted(mat_row) for mat_row in mat]
# print(len(sorted_mat))

### ---------------------------- DISPLAY ---------------------------------------
display = False
if display: 
    blank_img = np.zeros((918, 1398, 3))
    color = 1
    for row in sorted_mat:
        color += 1
        for red_dot in row:
            if color % 2 == 0:
                blank_img[red_dot[1]][red_dot[0]] = [0, 0, 255]
            else: 
                blank_img[red_dot[1]][red_dot[0]] = [0, 255, 0]

    cv2.imshow("Image", blank_img)
    cv2.waitKey(0)

### ----------- CONVERT COORDINATES FROM PIXELS TO PHYSICAL DIMENSIONS ---------
# Going to have trouble because this needs to be very precise

else:
    pixel_height = img_height / np.shape(img)[0]
    pixel_width = img_width / np.shape(img)[1]

    print("pixel height: " + str(pixel_height))
    print("pixel width: " + str(pixel_width))

    centers_coordinates_mat = [] # = [(pixel_x * pixel_width, pixel_y * pixel_height) for (pixel_x, pixel_y) in centers]# append coordinates to list

    for row in sorted_mat:
        centers_coordinates_mat.append([[pixel_x * pixel_width, pixel_y * pixel_height] for [pixel_x, pixel_y] in row]) # append coordinates to list

    print("center coordinates matrix: \n" + str(centers_coordinates_mat))



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

    row_idx = 1
    inc = 0
    for row in centers_coordinates_mat:
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