from nilearn.glm.first_level import FirstLevelModel
from nilearn import image
import pandas as pd
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from nilearn.plotting import plot_stat_map, plot_contrast_matrix, plot_design_matrix
from pathlib import Path
from AnalysisMethods.helper_funcs import make_labeled_data

path = 'fMRI_Data/sub-001/func/sub-001_task-Training_run-01_bold.nii'
fmri_img = image.load_img(path)
events_path = 'fMRI_Data/sub-001/func/sub-001_task-Training_run-01_events.tsv'

events = pd.read_csv(events_path, sep='\t', usecols=[0, 1, 2])
events.rename(columns={events.columns[2]: 'trial_type'}, inplace=True)
events['trial_type'] = events['trial_type'].str.strip("'") # remove single quotes from trial_type column
alfa = 615 / 410
events['onset'] = events['onset'] * alfa
events['onset'] = events['onset'].round().astype(int)
events['duration'] = events['onset'].shift(-1) - events['onset']
events['duration'].iloc[-1] = 22
events['duration'] = events['duration'].round().astype(int)

# print(events.tail(5))


fmri_glm = FirstLevelModel(
    t_r=1,
    noise_model="ar1",
    standardize=False,
    hrf_model="spm",
    drift_model="cosine",
    high_pass=0.01,
)

fmri_glm = fmri_glm.fit(fmri_img, events)
design_matrix = fmri_glm.design_matrices_[0]

contrast_matrix = np.eye(design_matrix.shape[1])
basic_contrasts = dict([(column, contrast_matrix[i])
                        for i, column in enumerate(design_matrix.columns)])

ims = None
for _, _, file in os.walk('fMRI_Data/sub-001/func/'):
    if file.endswith('.nii') and file.startswith('sub-001_task-Training_run'):
        path = os.path.join('fMRI_Data/sub-001/func/', file)
        events_path = os.path.join('fMRI_Data/sub-001/func/', file.replace('bold.nii', 'events.tsv'))
        images = make_labeled_data(path, events_path, mean=True)
        if ims is None:
            ims = images
        else:
            for key in images:
                ims[key] = image.mean_img([ims[key], images[key]])
                

        
        
        # print(images.keys())
        # for key in images:
        #     imags = images[key]
        #     # imags = resample_to_img(imags, path_anat, interpolation='linear')
        #     fmri_glm = FirstLevelModel(
        #         t_r=1,
        #         noise_model="ar1",
        #         standardize=False,
        #         hrf_model="spm",
        #         drift_model="cosine",
        #         high_pass=0.01,
        #     )
        #     fmri_glm = fmri_glm.fit(imags, events)
        #     design_matrix = fmri_glm.design_matrices_[0]

        #     contrast_matrix = np.eye(design_matrix.shape[1])
        #     basic_contrasts = dict([(column, contrast_matrix[i])
        #                             for i, column in enumerate(design_matrix.columns)])
        #     for key in basic_contrasts:
        #         print(f"{key}: {basic_contrasts[key]}")
        #     print(f"Contrast matrix: {basic_contrasts['disco'] - basic_contrasts['rock']}")
        #     contrast_def = basic_contrasts['disco'] - basic_contrasts['rock']
        #     z_map = fmri_glm.compute_contrast(contrast_def, output_type='z_score')
        #     mean_img = image.mean_img(imags)
        #     threshold = 2.0
        #     plot_stat_map(
        #         z_map,
        #         bg_img=mean_img,
        #         threshold=threshold,
        #         display_mode="z",
        #         cut_coords=3,
        #         black_bg=True,
        #         title=f"Disco minus Rock (Z>{threshold})"
        #     )
        #     plt.show()

# Specify your contrast; for example, comparing condition 'A' vs 'B'
cond_a, cond_b = 'rock', 'jazz'
contrast_def = basic_contrasts['rock'] - basic_contrasts['jazz']

# Compute the contrast
z_map = fmri_glm.compute_contrast(contrast_def, output_type='z_score')
# eff_map = fmri_glm.compute_contrast(contrast_def, output_type='effect_size')
mean_img = image.mean_img(fmri_img)
# plot_stat_map(z_map, threshold=0.8, display_mode='z', cut_coords=3, title='Condition A vs B')
# plot_contrast_matrix(contrast_def, design_matrix=design_matrix)
threshold = 2.0
plot_stat_map(
    z_map,
    bg_img=mean_img,
    threshold=threshold,
    display_mode="z",
    cut_coords=3,
    black_bg=True,
    title=f"{cond_a} minus {cond_b} (Z>{threshold})"
)
plt.show()
