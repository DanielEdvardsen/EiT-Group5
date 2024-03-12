import math

import numpy as np
import glm

# resolution
WIN_RES = glm.vec2(1600, 900)

# chunk
CHUNK_SIZE = 256
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE

# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)  # vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# player
PLAYER_SPEED = 0.1
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(0, 2, 5)
MOUSE_SENSITIVITY = 0.002

# colors
BG_COLOR = glm.vec3(0.1, 0.16, 0.25)