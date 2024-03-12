import numpy as np
import pywavefront

from meshes.base_mesh import BaseMesh


class BrainMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.brain

        self.vbo_format = "3f 3f 3f"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("in_color", "in_normal", "in_position")
        self.vao = self.get_vao()

    def get_vertex_data(self):
        objs = pywavefront.Wavefront(
            "renderer/objects/brains/sub-001_mesh.obj", cache=True, parse=True
        )
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype="f4")
        return vertex_data
