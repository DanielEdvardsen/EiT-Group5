import pandas as pd
from nilearn import image, plotting

events_path = 'fMRI_Data/sub-001/func/sub-001_task-Training_run-01_events.tsv'

events = pd.read_csv(events_path, sep='\t', usecols=[0, 1, 2])
events.rename(columns={events.columns[2]: 'trial_type'}, inplace=True)
events['trial_type'] = events['trial_type'].str.strip("'") # remove single quotes from trial_type column
# print(events.head(5))

path = 'fMRI_Data/sub-001/func/sub-001_task-Training_run-01_bold.nii'
images = {}
counter = 0
alfa = 410 / 615
while True:
    if (counter+1)*15*alfa > 410:
        break
    try:
        temp = image.index_img(path, slice(round(counter*15*alfa), round((counter+1)*15*alfa)))
        # print("Counter: ", counter, "slice: ", round(counter*15*alfa), round((counter+1)*15*alfa), "label: ", events['trial_type'][counter])
        label = events['trial_type'][counter]
        if label not in images:
            images[label] = temp
        else:
            images[label] = image.concat_imgs([images[label], temp])
        counter += 1
    except Exception as e:
        print(f"Exception: {e}")
        break
print(f"Ended on counter: {counter}")
for key in images:
    print(f"{key}: {images[key].shape}")
    images[key] = image.mean_img(images[key])
    print(f"{key}: {images[key].shape}")
    # plotting.plot_epi(images[key], title=f"Mean image for {key}")
# diff_image = image.math_img("img1 - img2", img1=img1, img2=img2)
# plotting.plot_stat_map(img1, title='Difference between img1 and img2')
diff_image = image.math_img("img1 - img2", img1=images['disco'], img2=images['rock'])
plotting.plot_stat_map(diff_image, title='Difference between disco and rock')
plotting.show()
