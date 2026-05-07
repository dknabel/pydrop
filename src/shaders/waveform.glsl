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
    vec2 diff = uv - center;
    
    // Sample frequency at this position
    float freq = texture(iFrequency, uv.x).r;
    
    // Calculate distance from center
    float dist = length(diff) * 2.0;
    
    // Waveform line
    float wave = abs(sin(uv.x * 10.0 - iTime) * 0.3);
    float line = smoothstep(0.1, 0.0, abs(dist - freq * 0.5 - wave));
    
    // Color based on frequency
    vec3 color = vec3(
        0.5 + 0.5 * sin(iTime + uv.x * 3.0),
        0.5 + 0.5 * sin(iTime + uv.y * 3.0 + 2.0),
        0.5 + 0.5 * sin(iTime + (uv.x + uv.y) * 3.0 + 4.0)
    );
    
    // Add audio reactivity
    color *= 0.5 + 0.5 * iAmplitude;
    color += freq * vec3(1.0, 0.5, 0.2);
    
    FragColor = vec4(color * line, line);
}
