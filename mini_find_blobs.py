def find_blobs(image):
    blobs = []
    visited = set()

    def dfs(pixel, blob):
        if pixel in visited:
            return
        visited.add(pixel)
        x, y = pixel
        if image[y][x] == [0, 0, 0]:
            blob.append(pixel)
            for neighbor in get_neighbors(pixel):
                dfs(neighbor, blob)

    def get_neighbors(pixel):
        x, y = pixel
        neighbors = []
        if x > 0:
            neighbors.append((x-1, y))
        if x < 59:
            neighbors.append((x+1, y))
        if y > 0:
            neighbors.append((x, y-1))
        if y < 59:
            neighbors.append((x, y+1))
        return neighbors

    for x in range(60):
        for y in range(60):
            pixel = (x, y)
            if pixel in visited:
                continue
            blob = []
            dfs(pixel, blob)
            if blob:
                blobs.append(blob)

    return blobs

import numpy as np
import cv2

img_1 = np.zeros((60,60, 3))
img_1 += 255
img_1[3][3] = [0,0,0]
img_1[3][4] = [0,0,0]
img_1[3][5] = [0,0,0]

img_1[4][3] = [0,0,0]
img_1[4][4] = [0,0,0]
img_1[4][5] = [0,0,0]

img_1[5][3] = [0,0,0]
img_1[5][4] = [0,0,0]
img_1[5][5] = [0,0,0]


img_1[13][3] = [0,0,0]
img_1[13][4] = [0,0,0]
img_1[13][5] = [0,0,0]

img_1[14][3] = [0,0,0]
img_1[14][4] = [0,0,0]
img_1[14][5] = [0,0,0]

img_1[15][3] = [0,0,0]
img_1[15][4] = [0,0,0]
img_1[15][5] = [0,0,0]

img_2 = (np.rint(img_1)).astype(int)

# blob_centers = find_blobs(img_2)
# print(blob_centers)
# print(img_2[13][4])

# for center in blob_centers:
#     img

# cv2.imshow("Image with Centers", img_1)
# cv2.waitKey(0)

