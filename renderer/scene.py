from pathlib import Path

from chunk import Chunk
from meshes.brain_mesh import BrainMesh
from meshes.skybox_mesh import SkyboxMesh

from settings import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []

        # the activation
        activation_01_path = Path("renderer/src/sub-001_activation-001.npy")
        self.objects.append(Chunk(self.app, activation_01_path))

        # the brain model
        self.objects.append(BrainMesh(self.app))

        # the skybox
        self.objects.append(SkyboxMesh(self.app))

    def update(self):
        pass

    def render(self):
        for obj in self.objects:
            obj.render()
