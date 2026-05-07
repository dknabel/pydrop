#version 330 core

uniform float iTime;
uniform vec2 iResolution;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform sampler1D iFrequency;

out vec4 FragColor;

// Hash function for pseudorandom
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// Noise function
float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    
    // Flowing particles
    vec2 p = uv * 5.0;
    float n = noise(p + iTime * 0.3);
    float n2 = noise(p - iTime * 0.2 + vec2(100.0));
    
    // Particle trails - modulated by audio
    float particle = exp(-length(fract(p + vec2(sin(iTime * n * (1.0 + iBass * 2.0)), cos(iTime * n2 * (1.0 + iTreble * 2.0))) - 0.5) * 3.0));

    // Frequency response
    float freq = texture(iFrequency, uv.x).r;
    particle *= freq * (0.5 + iAmplitude * 2.0);

    // Color - highly responsive to audio
    vec3 color = vec3(
        0.2 + 0.8 * sin(iTime * 0.5 + uv.x * 3.0 + iBass * 5.0),
        0.3 + 0.7 * sin(iTime * 0.5 + uv.y * 3.0 + 2.0 + iMid * 3.0),
        0.4 + 0.6 * sin(iTime * 0.5 + 4.0 + iTreble * 5.0)
    );

    // Audio boost
    color *= (1.0 + iBass * 3.0);
    color += iTreble * vec3(0.5, 1.0, 1.0) * 2.0;
    color += iMid * vec3(1.0, 0.5, 0.5) * 2.0;
    color *= 1.0 + iAmplitude * 2.0;

    FragColor = vec4(color, particle * (0.5 + iAmplitude * 2.0));
}
