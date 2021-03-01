from skimage import data, transform
import matplotlib.pyplot as plt
import numpy as np
img = data.camera()

# get transformation matrix
tform = transform.AffineTransform(scale=(0.9, 0.9), rotation=0.2, translation=(20, -10))

# apply the transform on the image
img_warped = transform.warp(img, tform.inverse)

#show the transformed image
fig, ax = plt.subplots(1, 2, figsize=(9, 6))
ax[0].imshow(img, cmap='gray')
ax[0].set_title('Original'), ax[0].axis('off')
ax[1].imshow(img_warped, cmap='gray')
ax[1].set_title('Warped'), ax[1].axis('off')
fig.tight_layout()
plt.show()

# Identify x,y points on the image
img_points = np.array([[250, 123], [401, 219], [131, 468], [433, 344]])
# identify corresponding x, y points on the warmed image (question how do we do this automatically?)
img_warped_points = np.array([[220, 145], [335, 256], [53, 428], [340, 372]])

fig, ax = plt.subplots(1, 2, figsize=(9, 6))
ax[0].imshow(img, cmap='gray')
ax[0].set_title('Original'), ax[0].axis('off')

# plot the points over the image
ax[0].plot(img_points[:, 0], img_points[:, 1], 'xr')
ax[1].imshow(img_warped, cmap='gray')

# plot the points over the image
ax[1].plot(img_warped_points[:, 0], img_warped_points[:, 1], 'xb')
ax[1].set_title('Warped'), ax[1].axis('off')
fig.tight_layout()
plt.show()

# Prepare to get the required transformation to match the img points to the corresponding points on transformed image
tform3 = transform.AffineTransform()
tform3.estimate(img_points, img_warped_points) # Here its done
img_aligned = transform.warp(img_warped, tform3) # apply the transformation and get new image

# how them all
fig, ax = plt.subplots(1, 3, figsize=(14, 6))
ax[0].imshow(img, cmap='gray'), ax[0].set_title('Original'), ax[0].axis('off')
ax[0].plot(img_points[:, 0], img_points[:, 1], 'xr')
ax[1].imshow(img_warped, cmap='gray'), ax[1].set_title('Warped'), ax[1].axis('off')
ax[1].plot(img_warped_points[:, 0], img_warped_points[:, 1], 'xb')
ax[2].imshow(img_aligned, cmap='gray'), ax[2].set_title('Aligned'), ax[2].axis('off')
fig.tight_layout()
plt.show()