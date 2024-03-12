# EiT-Group5

Visualizing fMRI data and displaying it on a website, goals are subject to change.

To install the neccesary dependencies run the command 'pip install -r requirements.txt'

Reference for the data used: 'Tomoya Nakai and Naoko Koide-Majima and Shinji Nishimoto (2021). Music Genre fMRI Dataset. OpenNeuro. [Dataset] doi: 10.18112/openneuro.ds003720.v1.0.0'

## Renderer

To run the renderer, run `main.py` in the `renderer` directory. The directory includes some left-over code and
is not documented well. This can be fixed later.

To generate a new mesh (activation voxels) use the file `chunk_mesh_builder.py` (look at the bottom on the
file, in the main loop).

Setting the brain model is done in `meshes/brain_mesh.py`. It uses an obj format.

Objects can be placed in the scene in `scene.py`. The scene is a list of objects. Here it is possible to add
multiple activation meshes for example. It should be self-explanatory how to change the activation.

The requirements for the renderer is in `renderer/requirements.txt`. They might not be 100% correct :D.
