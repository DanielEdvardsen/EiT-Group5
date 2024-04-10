import copy

from settings import *


class Camera:
    def __init__(self, position, yaw, pitch):
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def rotate_x(self, delta_x):
        # rotate around 0, 0, 0
        # pre_pos = self.position * 0.45
        # self.position -= glm.vec3(pre_pos)
        self.position = glm.rotate(
            self.position,
            delta_x,
            glm.vec3(
                0,
                1,  # glm.cos(self.pitch - glm.pi() / 2),
                0,  # glm.sin(self.pitch - glm.pi() / 2),
            ),
        )
        # rotate yaw
        self.rotate_yaw(-delta_x * 1.0)
        # self.position += glm.vec3(pre_pos)
        print(self.yaw)

    def rotate_y(self, delta_y):
        if self.pitch - delta_y > PITCH_MAX or self.pitch - delta_y < -PITCH_MAX:
            return
        self.position = glm.rotate(
            self.position,
            delta_y,
            glm.vec3(
                glm.cos(self.yaw - glm.pi() / 2), 0, glm.sin(self.yaw - glm.pi() / 2)
            ),
        )
        # rotate pitch
        self.rotate_pitch(delta_y * 1)
        # self.position += glm.vec3(pre_pos)

    def move_left(self, velocity):
        self.position -= self.right * velocity

    def move_right(self, velocity):
        self.position += self.right * velocity

    def move_up(self, velocity):
        self.position += self.up * velocity

    def move_down(self, velocity):
        self.position -= self.up * velocity

    def move_forward(self, velocity):
        self.position += self.forward * velocity

    def move_back(self, velocity):
        self.position -= self.forward * velocity
