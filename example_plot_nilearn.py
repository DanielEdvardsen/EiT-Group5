import nilearn
import os
from nilearn import image, plotting

path = 'fMRI_Data/sub-001/func/sub-001_task-Test_run-01_bold.nii'
img = image.load_img(path)
print(img.shape)
img = image.index_img(path, slice(0,15))
print(img.shape)
# firstSlice = image.index_img(path, slice(0, 2))
slices = []
while True:
    try:
        slices.append(image.index_img(path, slice(0, 15)))
    except:
        break
for slice in slices:
    print(slice.shape)
print(len(slices))
    # for img in image.iter_img(slice):
    #     plotting.plot_epi(img)

plotting.show()