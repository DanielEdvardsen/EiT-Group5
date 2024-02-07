import nilearn
import os
from nilearn import image, plotting

path = 'fMRI_Data/sub-001/func/sub-001_task-Test_run-01_bold.nii'
# img = nilearn.image.load_img(path)
firstSlice = image.index_img(path, slice(0, 2))

for img in image.iter_img(firstSlice):
    plotting.plot_epi(img)

plotting.show()