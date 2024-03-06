import pandas as pd
from nilearn import image

def make_labeled_data(path=str, events_path=str, mean=False):
    """
    path: str
        Path to the fMRI data
    events_path: str
        Path to the events.tsv file
    mean: bool
    
    Takes in the path to the fMRI data and the path to the events.tsv file 
    and returns a dictionary of images, where the keys are the labels and the
    values are the images corresponding to that label. i.e dict['disco'] gives
    a 4D image of all the disco images.
    
    if mean is True, then the images are averaged across the 4th dimension, 
    giving a single 3D image for each key.
    """
    events = pd.read_csv(events_path, sep='\t', usecols=[0, 1, 2])
    events['genre'] = events['genre'].str.strip("'")
    images = {}
    counter = 0
    # alfa = 410 / 615
    while True:
        if (counter+1)*10 > 410:
            break
        try:
            temp = image.index_img(path, slice(round(counter*10), round((counter+1)*10)))
            # print("Counter: ", counter, "slice: ", round(counter*15*alfa), round((counter+1)*15*alfa), "label: ", events['genre'][counter])
            label = events['genre'][counter]
            if label not in images:
                images[label] = temp
            else:
                images[label] = image.concat_imgs([images[label], temp])
            counter += 1
        except Exception as e:
            print(f"Exception: {e}")
            break
    if mean:
        for key in images:
            images[key] = image.mean_img(images[key])
    return images