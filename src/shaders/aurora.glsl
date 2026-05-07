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

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    
    // Aurora waves
    float wave1 = sin(uv.x * 3.0 + iTime * 0.3) * sin(uv.y * 2.0 - iTime * 0.2);
    float wave2 = sin(uv.x * 5.0 - iTime * 0.4) * cos(uv.y * 3.0 + iTime * 0.25);
    float wave3 = sin((uv.x + uv.y) * 4.0 + iTime * 0.35) * 0.5;
    
    float freq = texture(iFrequency, uv.x).r;
    
    // Combine waves
    float aurora = (wave1 + wave2 + wave3) * 0.5;
    aurora += freq * (uv.y - 0.3) * 2.0;
    
    // Color palette for aurora
    vec3 color = vec3(0.0);
    color += vec3(0.0, 1.0, 0.5) * smoothstep(0.3, 0.6, aurora) * iBass;
    color += vec3(0.0, 0.5, 1.0) * smoothstep(0.0, 0.3, aurora);
    color += vec3(1.0, 0.0, 0.5) * smoothstep(0.6, 1.0, aurora) * iTreble;
    
    FragColor = vec4(color, max(aurora, 0.3));
}
