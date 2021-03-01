from scipy import ndimage
from skimage import io, segmentation, feature
import matplotlib.pyplot as plt
import numpy as np

# Generate an initial image with two overlapping circles
# Note that the image is boolean, mimicking the result of a potential thresholding
x, y = np.indices((80, 80))
x1, y1, x2, y2 = 28, 28, 44, 52
r1, r2 = 16, 20
mask_circle1 = (x - x1)**2 + (y - y1)**2 < r1**2
mask_circle2 = (x - x2)**2 + (y - y2)**2 < r2**2
img = np.logical_or(mask_circle1, mask_circle2)

plt.figure(figsize=(6, 6))
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.show()

# First, we need to apply the distance transform to the binary image
# ...the distance per pixel to the nearest zero
# black is zero in image
distance = ndimage.distance_transform_edt(img)

print(distance)

# Next, we generate the markers as local maxima of the distance image
# (This is equivalent to generating the local minima of the -distance image)
#coords = feature.peak_local_max(distance, footprint=np.ones((3, 3)), labels=img)
maxima_coords = feature.peak_local_max(distance)
mask = np.zeros(distance.shape, dtype=bool)
mask[tuple(maxima_coords.T)] = True
markers, _ = ndimage.label(mask)

# We can then run the watershed algorithm
labels = segmentation.watershed(-distance, markers, mask=img)

fig, ax = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True)

ax[0].imshow(img, cmap=plt.cm.gray)
ax[0].set_title('Overlapping objects'), ax[0].axis('off')
pos = ax[1].imshow(-distance, cmap='gray')
ax[1].set_title('(Neg.) Distance transform')
ax[1].axis('off'), ax[1].set_aspect('auto')
ax[2].imshow(labels)
ax[2].set_title('Separated objects'), ax[2].axis('off')
fig.colorbar(pos, ax=ax[1])
fig.tight_layout()
plt.show()