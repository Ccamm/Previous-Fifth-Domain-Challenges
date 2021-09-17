import numpy as np
import cv2

img = cv2.imread("pm.png")
print(img.shape)
print(np.unique(img))

for x in img:
    print(x)
