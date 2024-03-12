#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 u_color;
// in vec3 normal;
// in vec3 fragPos;


uniform sampler2D u_texture_0;
// uniform vec3 camPos;
// uniform vec2 u_resolution;


void main() {
    // float gamma = 2.2;
    // vec3 color = texture(u_texture_0, uv_0).rgb;
    // color = pow(color, vec3(gamma));
    // color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(u_color, 0.5);
}