#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 voxel_c;
layout (location = 2) in float face_id;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 voxel_color;


void main() {
    int uv_index = 1;//gl_VertexID % 6  + (face_id & 1.0) * 6;
    voxel_color = voxel_c;
    vec3 pos = in_position - vec3(100.0, 150.0, 115.0);
    gl_Position = m_proj * m_view * m_model * vec4(pos, 1.0);
}







































