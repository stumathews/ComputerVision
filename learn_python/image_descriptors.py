from skimage import data, img_as_ubyte, transform
import numpy as np
import cv2
import matplotlib.pyplot as plt

img = img_as_ubyte(data.camera())  # Format required by OpenCV

# get transformation matrix
# Note the changing the scale or orentation does not affect the detection and matching of features using SIFT
tform = transform.AffineTransform(scale=(0.8, 0.8), rotation=0.5, translation=(20, -10))
# transform the image
img_warped = img_as_ubyte(transform.warp(img, tform.inverse))

fig, ax = plt.subplots(1, 2, figsize=(9, 6))
ax[0].imshow(img, cmap='gray')
ax[0].set_title('Original'), ax[0].axis('off')
ax[1].imshow(img_warped, cmap='gray')
ax[1].set_title('Warped'), ax[1].axis('off')
fig.tight_layout()
plt.show()

# Initiate SIFT detector
sift = cv2.SIFT_create()

# find the keypoints and descriptors with SIFT. These matches should be
# orientation invarient
kp1, des1 = sift.detectAndCompute(img, None)
kp2, des2 = sift.detectAndCompute(img_warped, None)

print(kp1)
# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

# Match descriptors - This is quite important.
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)

# Remove not so good matches
good_match_ratio = 0.5
numGoodMatches = int(len(matches) * good_match_ratio)
matches = matches[:numGoodMatches]

# Show matches
fig = plt.figure(figsize=(12, 9))
# draw the keypoints for orignal image and transfomed images, and hook-up matches
imMatches = cv2.drawMatches(img, kp1, img_warped, kp2, matches, None)
plt.imshow(imMatches)
plt.show()

# Extract points (x,y) of good matches
points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

for i, match in enumerate(matches):
    points1[i, :] = kp1[match.queryIdx].pt
    points2[i, :] = kp2[match.trainIdx].pt

# cv.findHomography() returns a mask which specifies the inlier and outlier points - https://docs.opencv.org/master/d1/de0/tutorial_py_feature_homography.html
# If we pass the set of points from both the images, it will find the perspective transformation of that object.
inv_h, _ = cv2.findHomography(points1, points2, cv2.RANSAC)

# Align the image, using the perspective transformation of that object
img_aligned = transform.warp(img_warped, inv_h)

# Note because SIFT uses DOG to simulate scaling to pick out the key points, it is rotation and scale invariant!
# Changing the scale and rotation of warped image does not affect the keypoints matched on the other scaled/rotated/warped image
# So the matches are found still, becasue the matches are chosen using DOG which makes them robust!

fig, ax = plt.subplots(1, 3, figsize=(14, 6))
ax[0].imshow(img, cmap='gray')
ax[0].set_title('Original'), ax[0].axis('off')
ax[1].imshow(img_warped, cmap='gray')
ax[1].set_title('Warped'), ax[1].axis('off')
ax[2].imshow(img_aligned, cmap='gray')
ax[2].set_title('Aligned'), ax[1].axis('off')
fig.tight_layout()
plt.show()