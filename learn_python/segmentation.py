# Task 1.2 : Segmentation
from skimage import io, img_as_float, img_as_ubyte
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, color, filters
import numpy as np
from skimage import color, img_as_float, img_as_ubyte
from skimage import io, color, filters
from scipy.ndimage import binary_fill_holes
from skimage import measure, color
from sklearn.cluster import KMeans
from numpy import where
# load in the picture
img = io.imread('OnTheBeach.png')

# Get rid of some of the detail
img = img_as_ubyte(filters.gaussian(img, sigma=1))
rows, cols, _ = img.shape

# Segmentation map
img_seg = np.ndarray([rows, cols])

for r in range(rows):
    for c in range(cols):
        red = img[r][c][0]
        green = img[r][c][1]
        blue = img[r][c][2]
        img_seg[r, c] = 1 if red > 155 and 180 > green > 100 and blue < 140 else 0


fig, ax = plt.subplots(1, 2)

ax[0].imshow(img)
ax[1].imshow(img_seg, cmap='gray')
plt.show()

im_filled = binary_fill_holes(img_as_float(img_seg))

plt.figure(figsize=(9, 6))
plt.imshow(im_filled, cmap='gray')
plt.axis('off')
plt.show()

label_img = measure.label(im_filled)
label_img_rgb = color.label2rgb(label_img, bg_label=0)

plt.figure(figsize=(9, 6))
plt.imshow(label_img_rgb)
plt.axis('off')
plt.show()

print(f'label_img: dtype={label_img.dtype} shape={label_img.shape}')
print(f'label_img_rgb: dtype={label_img_rgb.dtype} shape={label_img_rgb.shape}')

regions = measure.regionprops(label_img)

area_T = 1000
region_ids = [props.label for props in regions if props.area > area_T ]
print(region_ids)


# label_img contains numbered/labled ids per pixel - make all region pixels that are not > 1000 black
label_img_filtered = np.array([px if px in region_ids else 0 for px in label_img.ravel()])
label_img_filtered = label_img_filtered.reshape(label_img.shape)
label_img_filtered_rgb = color.label2rgb(label_img_filtered, bg_label=0) # consider black as background(see above)
# should only have the non-background data left that is coloured in.

plt.figure(figsize=(9, 6))
plt.imshow(label_img_filtered_rgb)
plt.axis('off')
plt.show()

print(label_img_filtered_rgb.dtype)
print(label_img_filtered_rgb.shape)

#Task 1.3:  Improve  Improve region filtering
##############################################################################
# TODO: Improve region-based filtering                                       #
##############################################################################

# Two pixels are connected when they are neighbors and have the same value
# this labels [y][x] = n (a numeric label)
label_img = measure.label(im_filled)

# get the properties for those labels
region_props = measure.regionprops(label_img)

#for props in region_props:
#  print(f'Region {props.label}')
#  print(props.filled_area)

# keep regions less than 2000 filled area
region_ids = [props.label for props in region_props if props.area > 1000 and props.bbox_area > 4000]
print(region_ids)
for props in region_props:
  if props.label in region_ids:
    print(f'{props.label}: area={props.area}, bbox_area={props.bbox_area}')

# set the pixel label to 0, if its not one of our region_ids that we filted down to being > 1000, > 4000 etc
# we are left with only values for [y][x] that are for our identified shapes
# this is still a black and white image, but its not flattened ((159720,))
label_img_filtered = np.array([px if px in region_ids else 0 for px in label_img.ravel()])
# unflatten it to that of multi-d array
label_img_filtered = label_img_filtered.reshape(label_img.shape)
# Take our labled image ie [y][x] = n, and colour them in. ie have values insert into our rgb channels
label_img_filtered_rgb = color.label2rgb(label_img_filtered, bg_label=0)

plt.figure(figsize=(9, 6))
plt.imshow(label_img_filtered_rgb)
plt.axis('off')
plt.show()

label_img_filtered_rgb = color.label2rgb(label_img_filtered, image=img, bg_label=0)

plt.figure(figsize=(9, 6))
plt.imshow(label_img_filtered_rgb)
plt.axis('off')
plt.show()


img_reshaped = img_as_float(img).reshape((img.shape[0] * img.shape[1], 3))
print('Img_reshaped shape =', img_reshaped.shape)

n_colours = 6
kmeans = KMeans(n_clusters=n_colours, random_state=0).fit(img_reshaped)
labels = kmeans.predict(img_reshaped)

img_seg2 = kmeans.cluster_centers_[labels]
img_seg2 = img_as_ubyte(img_seg2.reshape(img.shape))

fig, ax = plt.subplots(ncols=2, figsize=(18, 6))
ax[0].imshow(img), ax[0].axis('off')
ax[1].imshow(img_seg2), ax[1].axis('off')
fig.tight_layout()
plt.show()

# how good is your segmentation?
result = img_as_float(label_img_filtered > 0)
gt = io.imread('GroundTruth.png')
gt = img_as_float(color.rgb2gray(gt))

fig, ax = plt.subplots(ncols=2, figsize=(18, 6))
ax[0].imshow(gt, cmap='gray')
ax[0].axis('off'), ax[0].set_title('Ground-truth')
ax[1].imshow(result, cmap='gray')
ax[1].axis('off'), ax[1].set_title('Our result')
fig.tight_layout()
plt.show()

# Task 2.1 Computing classification-based metrics
##############################################################################
# TODO: Compute classification-based metrics                                 #
##############################################################################


flat_gt = gt.ravel()
flat_my = result.ravel()

unique, counts = np.unique(flat_gt, return_counts=True)
gt_counts = dict(zip(unique, counts))
print(f'gt_counts: {gt_counts}')

unique, counts = np.unique(flat_my, return_counts=True)
my_counts = dict(zip(unique, counts))
print(f'my_counts: {my_counts}')


tp = 0 # both gt and my are forground for same pixel
tn = 0 # both gt and my are background or same pixel
fp = 0 # gt says background, mines says foregound
fn = 0 # gt says foregound, mines says background

if len(flat_gt) == len(flat_my):
  for i in range(len(flat_gt)):
      same = flat_gt[i] == flat_my[i]
      is_fg_in_gt = flat_gt[i] == 1.0
      if same:
        # tp,tn
        if is_fg_in_gt:
          tp += 1
        else:
          tn += 1 #
      else:
        # fn/fp
        if is_fg_in_gt:
          fn += 1
        else:
          fp += 1 #

  print(f'TP={tp}, TN={tn}, FN={fn}, FP={fp}')
  print(f'Accuracy: {(tp+tn)/(tp+tn+fp+fn)}')
  print(f'Sensitivity: {tp/(tp+fn)}')
  print(f'Specififity: {tn/(tn+fp)}')

##############################################################################
#                             END OF YOUR CODE                               #
##############################################################################

# Task 2.2: Computing the Dice-Sørensen Coefficient (DSC)
##############################################################################
# TODO: Compute DSC                                                          #
##############################################################################
print(f'DSC:{(2 * tp)/ ((2*tp) + fp + fn)}')
##############################################################################
#                             END OF YOUR CODE                               #
##############################################################################