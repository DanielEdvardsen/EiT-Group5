from meshes.skybox_mesh import SkyboxTexture
from settings import *


class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.player = app.player
        # -------- shaders -------- #
        self.chunk = self.get_program(shader_name="chunk")
        self.skybox = self.get_program(shader_name="skybox")
        self.brain = self.get_program(shader_name="brain")
        self.skybox_texture = SkyboxTexture(app)
        # ------------------------- #
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        # chunk
        self.chunk["m_proj"].write(self.player.m_proj)
        self.chunk["m_model"].write(glm.mat4())

        # brain
        self.brain["m_proj"].write(self.player.m_proj)
        self.brain["m_model"].write(glm.mat4())

        # skybox
        self.texture = self.skybox_texture.texture
        self.skybox["u_texture_skybox"] = 0
        self.texture.use(location=0)
        self.skybox["m_proj"].write(self.player.m_proj)
        self.skybox["m_view"].write(glm.mat4(glm.mat3(self.player.m_view)))

    def update(self):
        self.chunk["m_view"].write(self.player.m_view)
        self.brain["m_view"].write(self.player.m_view)
        self.skybox["m_view"].write(glm.mat4(glm.mat3(self.player.m_view)))

    def get_program(self, shader_name):
        with open(f"renderer/shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"renderer/shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program
