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

// Simplex-like noise approximation
float noise(vec2 p) {
    return fract(sin(p.x * 12.9898 + p.y * 78.233) * 43758.5453);
}

// Turbulent flow field
void main() {
    vec2 pos = uv;

    // Turbulence intensity controlled by bass
    float turbIntensity = iBass * 2.0;

    // Swirl controlled by mid
    float swirl = iMid * iTime;
    vec2 offset = vec2(sin(swirl), cos(swirl)) * turbIntensity;

    // Add flowing motion
    pos += offset + vec2(iTime * 0.1, sin(iTime * 0.15) * 0.2);

    // Multi-octave noise for detail
    float n = 0.0;
    float amp = 1.0;
    for (int i = 0; i < 4; i++) {
        n += amp * sin(noise(pos * (1.0 + float(i) * iTreble)));
        pos *= 2.0;
        amp *= 0.5;
    }

    // Normalize and apply amplitude
    n = n / 1.875;
    n = smoothstep(0.3, 0.7, n);

    // Color based on turbulence pattern
    vec3 color = mix(
        mix(color0, color1, n),
        mix(color2, color3, sin(n * 3.14159) * 0.5 + 0.5),
        0.5
    );

    // Final output with amplitude control
    fragColor = vec4(color * n * iAmplitude, n * iAmplitude);
}
