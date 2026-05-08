#version 330 core

uniform float iTime;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform vec2 iResolution;

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
    float scale = 1.0 + iBass * 0.5;
    pos /= scale;

    // Rotation controlled by mid
    float angle = iMid * iTime * 2.0;
    mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
    pos = rot * pos;

    // Create grid pattern
    vec2 grid = fract(pos);
    vec2 gridDist = min(grid, 1.0 - grid);
    float gridLine = min(gridDist.x, gridDist.y);

    // Add detail controlled by treble
    float detail = iTreble * 0.3;
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
    float brightness = (gridLine + glow * 0.5) * iAmplitude;
    fragColor = vec4(color * brightness, brightness);
}
