import numpy as np
import pygame as pg

from meshes.base_mesh import BaseMesh


class SkyboxTexture:
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.texture = self.get_texture_cube("renderer/textures/skybox1", "png")

    def get_vertex_data(self):
        vertices = [
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
        ]
        indices = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]
        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.flip(vertex_data, 1).copy(order="C")
        return vertex_data

    @staticmethod
    def get_data(verices, indices):
        return np.array(
            [verices[ind] for triangle in indices for ind in triangle], dtype="f4"
        )

    def get_texture_cube(self, dir_path, ext="png"):
        faces = ["right", "left", "top", "bottom"] + ["front", "back"][::-1]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f"/{face}.{ext}").convert()
            if face in ["right", "left", "front", "back"]:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], "RGB")
            texture_cube.write(face=i, data=texture_data)

        return texture_cube


class SkyboxMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader_program.skybox

        self.vbo_format = "3f"
        self.attrs = ["in_position"]
        self.vao = self.get_vao()
        self.texture = self.get_texture_cube("renderer/textures/skybox1", "png")

    def get_vertex_data(self):
        vertices = [
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
        ]
        indices = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]
        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.flip(vertex_data, 1).copy(order="C")
        return vertex_data

    @staticmethod
    def get_data(verices, indices):
        return np.array(
            [verices[ind] for triangle in indices for ind in triangle], dtype="f4"
        )

    def get_texture_cube(self, dir_path, ext="png"):
        faces = ["right", "left", "top", "bottom"] + ["front", "back"][::-1]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f"/{face}.{ext}").convert()
            if face in ["right", "left", "front", "back"]:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], "RGB")
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = self.ctx.texture_cube(
            size=texture.get_size(),
            components=3,
            data=pg.image.tostring(texture, "RGB", False),
        )
        return texture
