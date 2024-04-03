import numpy as np
import pywavefront
from meshes.base_mesh import BaseMesh


class BrainMesh(BaseMesh):
    def __init__(self, app, subject_id=1):
        super().__init__()
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.brain
        self.subject_id = subject_id

        self.vbo_format = "3f 3f 3f"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("in_color", "in_normal", "in_position")
        self.vao = self.get_vao()

    def get_vertex_data(self):
        print(f"subjectId-> + {self.subject_id}")
        objs = pywavefront.Wavefront(
            f"src/constructions/sub_00{self.subject_id}/sub-00{self.subject_id}_mesh.obj",
            cache=True,
            parse=True,
        )
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype="f4")
        return vertex_data
