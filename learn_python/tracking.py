from skimage.measure import label, regionprops
import cv2
import numpy as np
import matplotlib.pyplot as plt
cap = cv2.VideoCapture('GregPen.avi')
#cap = cv2.VideoCapture(os.path.join(GOOGLE_DRIVE_PATH, 'GregPen.avi'))
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f'frameCount: {frameCount}, frameWidth: {frameWidth}, frameHeight: {frameHeight}')

video = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

fc = 0
ret = True

while fc < frameCount and ret:
    ret, video[fc] = cap.read()
    video[fc] = cv2.cvtColor(video[fc], cv2.COLOR_BGR2RGB)
    fc += 1
    # perform segmentation on this frame

marker_coord = np.zeros((frameCount, 2))
for i in range(frameCount):
    # Create segmentation map
    img_seg = (video[i, :, :, 0] > 190) \
              & (video[i, :, :, 1] > 40) & (video[i, :, :, 1] < 120) \
              & (video[i, :, :, 2] > 120) & (video[i, :, :, 2] < 210)

    # label the image
    label_img = label(img_seg)
    # get regions per label
    regions = regionprops(label_img)
    sorted_regions = sorted(regions, key=lambda x: x.area, reverse=True)
    marker_coord[i, :] = sorted_regions[0].centroid

cap.release()

# Plot the diffirent frames and the associated marker for that frame
fig, ax = plt.subplots(1, 3, figsize=(14, 6))
ax[0].imshow(video[1, :, :, :])
ax[0].plot(marker_coord[1, 1], marker_coord[1, 0], 'og')
ax[0].set_title('Frame1'), ax[0].axis('off')
ax[1].imshow(video[200, :, :, :])
ax[1].plot(marker_coord[200, 1], marker_coord[200, 0], 'og')
ax[1].set_title('Frame200'), ax[1].axis('off')
ax[2].imshow(video[299, :, :, :])
ax[2].set_title('Frame299'), ax[2].axis('off')
ax[2].plot(marker_coord[299, 1], marker_coord[299, 0], 'og')
fig.tight_layout()
plt.show()

from matplotlib import rc
import matplotlib
import matplotlib.animation as animation

matplotlib.use("qt5Agg")
rc('animation')

fig, ax = plt.subplots()

def frame(i):
    ax.clear()
    ax.axis('off')
    fig.tight_layout()
    plot=ax.imshow(video[i, :, :, :])
    return plot

anim = animation.FuncAnimation(fig, frame, frames=100)
plt.close()
anim