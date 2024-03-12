from settings import *
from meshes.chunk_mesh import ChunkMesh


class Chunk:
    def __init__(self, app, path):
        self.app = app
        self.mesh: ChunkMesh = None
        self.mesh_path = path
        self.build_mesh()

    def build_mesh(self):
        self.mesh = ChunkMesh(self, self.mesh_path)

    def render(self):
        self.mesh.render()
