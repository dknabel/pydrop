#version 330 core

uniform float iTime;
uniform vec2 iResolution;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform sampler1D iFrequency;

out vec4 FragColor;

float random(float x) {
    return fract(sin(x * 12.9898) * 43758.5453);
}

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    
    // Glitch displacement
    float glitch = random(floor(iTime * 20.0)) * iAmplitude * 2.0;
    float glitchX = sin(uv.y * 10.0 + glitch) * glitch * 0.1;
    
    vec2 glitchUv = uv + vec2(glitchX, 0.0);
    
    // RGB split
    float r = texture(iFrequency, glitchUv.x + 0.01).r;
    float g = texture(iFrequency, glitchUv.x).r;
    float b = texture(iFrequency, glitchUv.x - 0.01).r;
    
    // Scan lines
    float scanline = sin(uv.y * 100.0 + iTime * 10.0) * 0.3 + 0.7;
    
    // Frequency bars
    float bars = floor(uv.y * 8.0) / 8.0;
    float freq = texture(iFrequency, bars).r;
    
    // Digital effect
    float digital = step(0.5, fract(uv.x * 20.0 + iTime));
    
    vec3 color = vec3(r, g, b);
    color *= scanline;
    color *= 1.0 + freq * iBass * 2.0;
    color *= digital * 0.7 + 0.3;
    color += random(iTime + uv.x) * glitch * 0.2;
    
    FragColor = vec4(color, 1.0);
}
