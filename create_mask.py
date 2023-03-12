# import cv2
# import numpy as np

# # create a black image with dimensions (512, 512) and 3 color channels
# img = np.zeros((512, 512, 3), np.uint8)

# # draw a circle with center (256, 256), radius 100, color (0, 0, 255), and thickness 2
# cv2.circle(img, (256, 256), 100, (0, 0, 255), 2)

# # show the image
# cv2.imshow("image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

##########################################



# import cv2

# # Load the images
# img1 = cv2.imread('images/trial_1 _seond_edit.jpg')
# img2 = cv2.imread('images/plate_with_paper.jpg')

# # Resize the images to the same size
# img1 = cv2.resize(img1, (640, 480))
# img2 = cv2.resize(img2, (640, 480))

# # Blend the images together
# alpha = 0.5
# beta = 1 - alpha
# output = cv2.addWeighted(img1, 1, img2, 1, 0)

# # Display the resulting image
# cv2.imshow('Superimposed Image', output)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

##########################################


# import cv2
# import numpy as np

# # Load the image
# img = cv2.imread('images/edited_dots_on_paper_1.jpg')

# # Create a black image of the same size as the original
# mask = np.zeros_like(img)

# # Set the center and radius of the circular mask
# center = (200, 200)
# radius = 100

# # Draw a white filled circle on the mask image
# cv2.circle(mask, center, radius, (255, 255, 255), -1)

# # Apply the mask to the original image to set all pixels outside of the circular region to white
# result = cv2.bitwise_and(img, mask)

# # Display the result
# cv2.imshow('Result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



##########################################


import cv2
import numpy as np

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
img = cv2.imread('images/edited_dots_on_paper_1.jpg')

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

cv2.imwrite("images/img_with_mask.jpg", masked_img)

# cv2.imshow("Image with Centers", masked_img)
# cv2.waitKey(0)

# close all windows
# cv2.destroyAllWindows()





