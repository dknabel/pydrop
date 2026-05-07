#version 330 core

uniform float iTime;
uniform vec2 iResolution;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform sampler1D iFrequency;

out vec4 FragColor;

float noise(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

float fbm(vec2 p) {
    float f = 0.0;
    float w = 0.5;
    for(int i = 0; i < 4; i++) {
        f += w * noise(p);
        p *= 2.0;
        w *= 0.5;
    }
    return f;
}

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;

    // Tunnel vision effect
    float pattern = length(uv - 0.5) - iTime * 0.2 + fbm(uv);

    // Audio response
    float audioResponse = iAmplitude * (iBass + iMid + iTreble) / 3.0;
    float freq = texture(iFrequency, uv.x).r;

    // Color mapping
    vec3 color = vec3(
        sin(pattern + iTime * 0.5 + freq) * 0.5 + 0.5,
        sin(pattern + iTime * 0.7 + audioResponse) * 0.5 + 0.5,
        cos(pattern + iTime * 0.3) * 0.5 + 0.5
    );

    float alpha = smoothstep(0.2, 0.8, pattern) * (0.5 + audioResponse);

    FragColor = vec4(color, alpha);
}
