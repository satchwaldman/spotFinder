import cv2
import numpy as np

# assume 'img' is the image with dots
img = cv2.imread('images/img_with_mask.jpg')

# create a list to store the centers of the dots
centers = []

def on_mouse_click(event, x, y, flags, param):
    global centers
    
    if event == cv2.EVENT_LBUTTONDOWN: # add a new point
        centers.append((x, y))
        # draw a small circle at the clicked position
        cv2.line(img, (x, y), (x, y), (0, 0, 255), 1)
    elif event == cv2.EVENT_RBUTTONDOWN: # remove a point
        for i in range(len(centers)):
            center = centers[i]
            if abs(center[0] - x) < 5 and abs(center[1] - y) < 5:
                del centers[i]
                break
        # redraw all the points
        img.fill(0)
        for center in centers:
            cv2.circle(img, center, 1, (0, 0, 255), -1)

cv2.namedWindow('image')
cv2.setMouseCallback('image', on_mouse_click)

while True:
    cv2.imshow('image', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        # cv2.imwrite("images/img_with_centers_added.jpg", img)
        print(centers)
        break

cv2.destroyAllWindows()