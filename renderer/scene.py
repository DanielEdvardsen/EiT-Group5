from pathlib import Path

from chunk import Chunk
from meshes.brain_mesh import BrainMesh
from meshes.skybox_mesh import SkyboxMesh

from settings import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []

        self.activations = []

        # the activation
        activation_path = Path("renderer/src/sub-001/run1")
        for activation in activation_path.iterdir():
            self.activations.append(Chunk(self.app, activation))

        # the brain model
        self.objects.append(BrainMesh(self.app))
        # add one more placeholder for mesh (being popped on first iteration)
        self.objects.append(BrainMesh(self.app))

        # the skybox
        self.objects.append(SkyboxMesh(self.app))

        self.t = 0

    def update(self, time):
        new_time = round(time)
        if new_time > self.t:
            self.t = new_time
            self.objects.pop(0)
            activation_idx = self.t % len(self.activations)
            self.objects.insert(0, self.activations[activation_idx])

    def render(self):
        for obj in self.objects:
            obj.render()
