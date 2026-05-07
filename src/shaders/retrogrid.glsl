#version 330 core

uniform float iTime;
uniform vec2 iResolution;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform sampler1D iFrequency;

out vec4 FragColor;

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    uv.x *= iResolution.x / iResolution.y;
    
    // Perspective grid
    float perspective = 1.0 / (1.0 + uv.y * 3.0);
    uv *= perspective;
    
    // Grid lines
    float grid = 0.0;
    grid += step(0.9, fract(uv.x * 10.0));
    grid += step(0.9, fract(uv.y * 10.0));
    
    // Distance from center
    float dist = length(uv - vec2(0.5));
    
    // Frequency response
    float freq = texture(iFrequency, uv.x).r;
    
    // Color based on distance and frequency
    vec3 color = vec3(0.0);
    color.x = 0.2 + 0.8 * freq * iBass;
    color.y = 0.1 + 0.6 * sin(iTime * 0.5);
    color.z = 0.3 + 0.7 * cos(iTime * 0.3);
    
    color *= grid * (1.0 + iAmplitude) * exp(-dist * 2.0);
    
    // Horizon glow
    color += vec3(1.0, 0.5, 0.2) * (1.0 - uv.y) * 0.5;
    
    FragColor = vec4(color, 1.0);
}
