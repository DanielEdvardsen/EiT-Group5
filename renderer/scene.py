import struct
from chunk import Chunk
from pathlib import Path

from meshes.brain_mesh import BrainMesh
from meshes.skybox_mesh import SkyboxMesh
from settings import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.brains = []
        self.cur_subject_id = 1

        # the activation
        activation_01_path = Path("renderer/src/sub-001_activation-001.npy")
        self.objects.append(Chunk(self.app, activation_01_path))

        # the brain model
        for subject_id in range(1, 6):
            self.brains.append(BrainMesh(self.app, subject_id=subject_id))

        # the skybox
        # self.objects.append(SkyboxMesh(self.app))

    def update(self):
        pass

    def update_subject(self, subject_id):
        self.cur_subject_id = subject_id

    def render(self, context):
        for obj in self.objects:
            obj.render()
        self.brains[self.cur_subject_id - 1].render()
