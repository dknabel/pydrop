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
    vec2 center = vec2(0.5);
    uv -= center;
    
    // Polar coordinates for kaleidoscope
    float r = length(uv);
    float a = atan(uv.y, uv.x);
    
    // Kaleidoscope symmetry
    float sides = 6.0;
    a = mod(a, 3.14159 / sides);
    
    // Convert back to cartesian
    uv = vec2(cos(a), sin(a)) * r;
    
    // Frequency response
    float freq = texture(iFrequency, r).r;
    
    // Pattern
    float pattern = sin(uv.x * 10.0 - iTime) * cos(uv.y * 10.0 + iTime);
    pattern += sin((r - iTime * 0.3) * 20.0);
    pattern = 0.5 + 0.5 * sin(pattern);
    
    // Audio reactivity
    pattern *= freq;
    pattern *= 1.0 + iAmplitude * 2.0;
    
    // Color based on angle and frequency
    vec3 color = vec3(
        0.5 + 0.5 * sin(a * 3.0 + iTime),
        0.5 + 0.5 * sin(r * 5.0 - iTime * 0.5),
        0.5 + 0.5 * sin((a + r) * 3.0 + iTime * 0.7)
    );
    
    color *= pattern;
    color += freq * iTreble * vec3(0.5, 0.3, 0.8);
    
    FragColor = vec4(color, 1.0);
}
