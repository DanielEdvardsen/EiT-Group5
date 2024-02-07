from nilearn import image, plotting
from nilearn.decomposition import CanICA
from nilearn.plotting import plot_prob_atlas

path = 'fMRI_Data/sub-001/func/sub-001_task-Training_run-01_bold.nii'
img = image.load_img(path)

canica = CanICA(
    n_components=20,
    memory="nilearn_cache",
    memory_level=2,
    verbose=10,
    mask_strategy="whole-brain-template",
    random_state=0,
    standardize="zscore_sample",
    n_jobs=2,
)
canica.fit(img)
canica_components_img = canica.components_img_

plot_prob_atlas(canica_components_img, title="CanICA components", view_type="filled_contours")

plotting.show()