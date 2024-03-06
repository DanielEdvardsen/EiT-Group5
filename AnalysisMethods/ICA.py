from nilearn import image, plotting
from nilearn.image import resample_to_img
from nilearn.decomposition import CanICA
from nilearn.plotting import plot_prob_atlas, plot_stat_map
from helper_funcs import make_labeled_data
import os

cwd = os.getcwd().replace('\\', '/') + '/'
print(cwd)
path = cwd + 'fMRI_Data/sub-001/func/sub-001_task-Training_run-01_bold.nii'
events_path = cwd + 'fMRI_Data/sub-001/func/sub-001_task-Training_run-01_events.tsv'
images = make_labeled_data(path, events_path, mean=False)
print(images.keys())

canica = CanICA(
    n_components=20,
    memory="nilearn_cache",
    memory_level=2,
    verbose=10,
    mask_strategy="whole-brain-template",
    random_state=0,
    standardize="zscore_sample",
    n_jobs=2,
    threshold="auto",
)
path_anat = 'fMRI_Data/sub-001/anat/sub-001_T1w.nii'

for key in images:
    imags = images[key]
    # imags = resample_to_img(imags, path_anat, interpolation='linear')
    canica.fit(images[key])
    canica_components_img = canica.components_img_
    # resampled_canica = resample_to_img(canica_components_img, path_anat, interpolation='linear')
    fig = plot_prob_atlas(canica_components_img, title=f"CanICA genre={key}", view_type="filled_contours", colorbar=True, cmap="black_blue")
    fig.savefig(f"Images/ICA_sub-001-run-01_{key}.png")
plotting.show()