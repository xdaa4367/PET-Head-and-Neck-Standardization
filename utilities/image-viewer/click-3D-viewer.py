"""
Image Viewer for 3D Numpy arrays such as PET scans.

Based on: https://matplotlib.org/gallery/animation/image_slices_viewer.html

The basic viewer will be extended so that the value of a voxel can
be saved in order to calculate the tumor-background-ratio (TBR) of a PET scan.

Idea:
- scroll through the PET scan
- click on the background (e.g., healthy liver tissue) -> the value of the voxel will be stored
- compute corrected/normalized images
"""


from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import argparse

plt.rcParams['image.cmap'] = 'gray_r'

coords = []


class IndexTracker(object):
    def __init__(self, ax, X, view):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        rows, cols, self.slices = X.shape

        self.view = view
        self.ind = 0

        # axial
        if self.view == 'a':
            self.im = ax.imshow(self.X[:, :, self.ind])

        # sagittal
        if self.view == 's':
            self.im = ax.imshow(self.X[self.ind, :, :])

        # coronal
        if self.view == "c":
            self.im = ax.imshow(self.X[:, self.ind, :])

        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        # axial
        if self.view == 'a':
            self.im.set_data(self.X[:, :, self.ind])

        # sagittal
        if self.view == 's':
            self.im.set_data(self.X[self.ind, :, :])

        # coronal
        if self.view == 'c':
            self.im.set_data(self.X[:, self.ind, :])

        ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()

    def onclick(self, event):
        global ix, iy, iz
        ix, iy = event.xdata, event.ydata
        iz = self.ind
        print('x = %d, y = %d, z = %d' % (ix, iy, iz))

        global coords
        coords.append((ix, iy, iz))

        fig.canvas.mpl_disconnect(cid)

        return coords


fig, ax = plt.subplots(1, 1)

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, default="", help="Path of directory containing npy-file")
parser.add_argument("-v", "--view", type=str, default="a", help="axial (a), sagittal (s) or coronal (c).")
args = parser.parse_args()
path = args.path
view = args.view

# Hard coded
# path = 'C:\\Users\\david.haberl\\PycharmProjects\\PET-Head-and-Neck-Standardization_work\\pet.npy'
# view = "a"

img = np.load(path)
X = img

tracker = IndexTracker(ax, X, view=view)

fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
cid = fig.canvas.mpl_connect('button_press_event', tracker.onclick)
plt.show()
