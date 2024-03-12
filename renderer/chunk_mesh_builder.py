import numpy as np

from settings import *


def is_void(voxel_pos, chunk_voxels):
    x, y, z = voxel_pos
    if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
        if chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y].any():
            return False
    return True


def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


def build_chunk_mesh(chunk_voxels, format_size):
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype="f4")
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_c = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_c.any():
                    continue

                # top face
                if is_void((x, y + 1, z), chunk_voxels):
                    # format: x, y, z, voxel_c, face_id
                    v0 = (x, y + 1, z, voxel_c[0], voxel_c[1], voxel_c[2], 0)
                    v1 = (x + 1, y + 1, z, voxel_c[0], voxel_c[1], voxel_c[2], 0)
                    v2 = (x + 1, y + 1, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 0)
                    v3 = (x, y + 1, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 0)

                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # bottom face
                if is_void((x, y - 1, z), chunk_voxels):
                    v0 = (x, y, z, voxel_c[0], voxel_c[1], voxel_c[2], 1)
                    v1 = (x + 1, y, z, voxel_c[0], voxel_c[1], voxel_c[2], 1)
                    v2 = (x + 1, y, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 1)
                    v3 = (x, y, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 1)

                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right face
                if is_void((x + 1, y, z), chunk_voxels):
                    v0 = (x + 1, y, z, voxel_c[0], voxel_c[1], voxel_c[2], 2)
                    v1 = (x + 1, y + 1, z, voxel_c[0], voxel_c[1], voxel_c[2], 2)
                    v2 = (x + 1, y + 1, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 2)
                    v3 = (x + 1, y, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), chunk_voxels):
                    v0 = (x, y, z, voxel_c[0], voxel_c[1], voxel_c[2], 3)
                    v1 = (x, y + 1, z, voxel_c[0], voxel_c[1], voxel_c[2], 3)
                    v2 = (x, y + 1, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 3)
                    v3 = (x, y, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void((x, y, z - 1), chunk_voxels):
                    v0 = (x, y, z, voxel_c[0], voxel_c[1], voxel_c[2], 4)
                    v1 = (x, y + 1, z, voxel_c[0], voxel_c[1], voxel_c[2], 4)
                    v2 = (x + 1, y + 1, z, voxel_c[0], voxel_c[1], voxel_c[2], 4)
                    v3 = (x + 1, y, z, voxel_c[0], voxel_c[1], voxel_c[2], 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front face
                if is_void((x, y, z + 1), chunk_voxels):
                    v0 = (x, y, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 5)
                    v1 = (x, y + 1, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 5)
                    v2 = (x + 1, y + 1, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 5)
                    v3 = (x + 1, y, z + 1, voxel_c[0], voxel_c[1], voxel_c[2], 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[: index + 1]


def build_voxels(points, colors):
    # empty chunk
    voxels = np.zeros((CHUNK_VOL, 3), dtype="f4")

    for i, point in enumerate(points):
        x, y, z = point
        x, y, z = int(x), int(y), int(z)
        # check on x, y, z
        voxels[x + CHUNK_SIZE * y + CHUNK_AREA * z] = np.array(colors[i], dtype="f4")

    return voxels


if __name__ == "__main__":
    # point to the numpy files containing the activated coordinates and colors
    # this function will generate a mesh and save it to the output directory defined on line 117
    points = np.load("renderer/src/input/activated_coords.npy")
    colors = np.load("renderer/src/input/activated_colors.npy")
    voxels = build_voxels(points, colors)
    mesh = build_chunk_mesh(voxels, 7)
    np.save("renderer/src/sub-001_activation-001.npy", mesh)
    print("Mesh saved!")
