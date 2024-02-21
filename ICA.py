import nibabel as nib
from nilearn import image, plotting
from nilearn.decomposition import CanICA
from nilearn.plotting import plot_prob_atlas, plot_stat_map
import csv

path = 'fMRI_Data/sub-001/func/sub-001_task-Training_run-01_bold.nii'
# img1 = image.load_img(path)
filename = 'fMRI_Data/sub-001/func/sub-001_task-Training_run-01_events.tsv'
genres = []
with open(filename, 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        genres.append(row[2])

genres.pop(0)  # Remove the header

    
        
# images = []
# while True:
#     try:
#         images.append(image.index_img(path, slice(0, 15)))
#     except:
#         break

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
# for i in range(0, 2):
# img = images[0]
path_anat = 'fMRI_Data/sub-001/anat/sub-001_T1w.nii'
i = 0
while True:
    try:
        img = image.index_img(path, slice(i*15, (i+1)*15))
        canica.fit(img)
        canica_components_img = canica.components_img_

        fig = plot_prob_atlas(canica_components_img, title=f"CanICA genre={genres[i]}", view_type="filled_contours", bg_img=path_anat, colorbar=True, cmap="black_blue")
        fig.savefig(f'Images/ICA_1-1_{i}({genres[i]}).png')
        i += 1
        # plotting.show()
    except Exception as e:
        print(f"Error: {e}")
        
        break

# plotting.show()