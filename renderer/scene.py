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

        self.activations = []

        self.play = False
        self.current_frame = 0
        self.ticks = 0

        # the activations
        for i in range(20):
            act = Path(f'dataset/sub-001/func/run1/activation-{i}.npy')
            self.activations.append(Chunk(self.app, act))

        # the brain model
        for subject_id in range(1, 6):
            self.brains.append(BrainMesh(self.app, subject_id=subject_id))

        # the skybox
        #self.objects.append(SkyboxMesh(self.app))

    def update(self):
        ...

    def toggle_anim(self, time):
        if not self.play:
            self.play = True #Play
            self.time = time
            print("Play")
        else:
            self.play = False #Pause
            print("Pause")

    def reset(self):
        self.play = False #Pause
        self.current_frame = 0
    
    def update_subject(self, subject_id):
        self.cur_subject_id = subject_id

    def render(self, context, elapsed):
        for obj in self.objects:
            obj.render()
        self.brains[self.cur_subject_id - 1].render()


        if self.play:
            if elapsed - self.time >= 1.5:
                self.current_frame = (self.current_frame + 1) % 20
                self.time = elapsed

        self.activations[self.current_frame].render()