import numpy as np

from meshes.base_mesh import BaseMesh


class ChunkMesh(BaseMesh):
    def __init__(self, chunk, path):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.chunk

        self.mesh_path = path

        self.vbo_format = "3f 3f 1f"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("in_position", "voxel_c", "face_id")
        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = np.load(self.mesh_path)
        return mesh
