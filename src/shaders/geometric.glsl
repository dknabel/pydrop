#version 330 core

uniform float time;
uniform float amplitude;
uniform float bass;
uniform float mid;
uniform float treble;

// Color uniforms
uniform vec3 color0;
uniform vec3 color1;
uniform vec3 color2;
uniform vec3 color3;

in vec2 uv;
out vec4 fragColor;

// Grid and geometric patterns
void main() {
    vec2 pos = uv * 10.0;  // Scale for grid

    // Scale controlled by bass
    float scale = 1.0 + bass * 0.5;
    pos /= scale;

    // Rotation controlled by mid
    float angle = mid * time * 2.0;
    mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
    pos = rot * pos;

    // Create grid pattern
    vec2 grid = fract(pos);
    vec2 gridDist = min(grid, 1.0 - grid);
    float gridLine = min(gridDist.x, gridDist.y);

    // Add detail controlled by treble
    float detail = treble * 0.3;
    gridLine = smoothstep(detail + 0.01, detail - 0.01, gridLine);

    // Glow effect
    float glow = exp(-length(grid - 0.5) * length(grid - 0.5) * 5.0);

    // Color interpolation
    vec3 color = mix(
        mix(color0, color1, pos.x),
        mix(color2, color3, pos.y),
        0.5
    );

    // Final output
    float brightness = (gridLine + glow * 0.5) * amplitude;
    fragColor = vec4(color * brightness, brightness);
}
