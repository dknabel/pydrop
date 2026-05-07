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
    
    // Multiple wave sources
    float wave1 = sin(length(uv - vec2(0.3, 0.5)) * 20.0 - iTime * 2.0);
    float wave2 = sin(length(uv - vec2(0.7, 0.5)) * 20.0 - iTime * 1.8);
    float wave3 = sin(length(uv - vec2(0.5, 0.2)) * 15.0 - iTime * 2.2);
    
    // Interference pattern
    float interference = abs(wave1) + abs(wave2) + abs(wave3);
    interference = sin(interference * 5.0 + iTime);
    
    // Frequency modulation
    float freq = texture(iFrequency, uv.x).r;
    interference *= freq * (1.0 + iAmplitude * 2.0);
    
    // Color based on interference
    vec3 color = vec3(
        0.5 + 0.5 * sin(interference + iTime * 0.5),
        0.5 + 0.5 * sin(interference + iTime * 0.7 + 2.0),
        0.5 + 0.5 * sin(interference + iTime * 0.3 + 4.0)
    );
    
    // Add bass intensity
    color *= 1.0 + iBass;
    
    FragColor = vec4(color, max(interference * 0.5, 0.3));
}
