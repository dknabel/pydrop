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

void main() {
    vec2 pos = uv;

    // Volumetric density controlled by bass
    float density = 0.1 + bass * 0.3;

    // Oscillation speed controlled by mid
    float oscSpeed = mid * 1.5;

    // Shimmer/sparkle controlled by treble
    float shimmer = treble * 2.0;

    // Create soft, drifting layers
    float layers = 0.0;
    for (int i = 0; i < 3; i++) {
        float layer = sin(pos.y * float(i) + time * oscSpeed) * 0.5 + 0.5;
        layer *= sin(pos.x * float(i) * 0.7 + time * oscSpeed * 0.7) * 0.5 + 0.5;
        layer = smoothstep(0.2, 0.8, layer);
        layers += layer / 3.0;
    }

    // Add sparkle/twinkle
    float sparkle = sin(pos.x * 20.0 + time * shimmer) * sin(pos.y * 20.0 + time * shimmer * 0.7);
    sparkle = smoothstep(0.4, 0.6, sparkle + 0.5);
    sparkle *= 0.3;

    // Combine layers and sparkle
    float glow = layers + sparkle;
    glow = smoothstep(0.1, 0.9, glow * density);

    // Color transition based on position and time
    vec3 color = mix(
        mix(color0, color1, sin(time * 0.3 + pos.x) * 0.5 + 0.5),
        mix(color2, color3, cos(time * 0.2 + pos.y) * 0.5 + 0.5),
        glow
    );

    // Soft glow with amplitude control
    float finalGlow = glow * amplitude;
    fragColor = vec4(color * finalGlow, finalGlow * 0.8);
}
