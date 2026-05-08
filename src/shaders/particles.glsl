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

// Pseudo-random function
float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

// Particle system shader
void main() {
    vec2 pos = uv;

    // Particle density controlled by bass
    float density = 0.1 + iBass * 0.5;

    // Particle speed controlled by mid
    float speed = iMid * 2.0;

    // Particle spread controlled by treble
    float spread = 0.1 + iTreble * 0.3;

    // Generate particles using noise
    vec2 particlePos = pos + vec2(sin(iTime * speed + pos.y * 10.0), cos(iTime * speed + pos.x * 10.0)) * spread;

    float particle = random(floor(particlePos * density)) * 0.5 + 0.5;
    particle = smoothstep(0.3, 0.7, particle);

    // Apply distance falloff
    float dist = length(particlePos - pos);
    particle *= exp(-dist * dist * 5.0);

    // Color based on particle position and time
    vec3 color = mix(
        mix(color0, color1, sin(iTime * 0.5 + particlePos.x * 3.0) * 0.5 + 0.5),
        mix(color2, color3, cos(iTime * 0.3 + particlePos.y * 3.0) * 0.5 + 0.5),
        particle
    );

    // Final color with amplitude controlling intensity
    fragColor = vec4(color * particle * iAmplitude, particle * iAmplitude);
}
