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
    uv = uv * 2.0 - 1.0;
    uv.x *= iResolution.x / iResolution.y;
    
    // Polar coordinates
    float r = length(uv);
    float a = atan(uv.y, uv.x);
    
    // Tunnel effect
    float tunnel = 1.0 / (r + 0.1);
    tunnel *= sin(a * 5.0 + iTime);
    
    // Depth based on frequency
    float freq = texture(iFrequency, (a + 3.14159) / (2.0 * 3.14159)).r;
    float depth = sin(r * 10.0 - iTime * 2.0 + freq * 5.0);
    
    // Color
    vec3 color = vec3(
        0.5 + 0.5 * sin(a + iTime * 0.5),
        0.5 + 0.5 * sin(a - iTime * 0.3 + 2.0),
        0.5 + 0.5 * sin(a + iTime * 0.7 + 4.0)
    );
    
    color *= tunnel * depth * (0.5 + iBass * 1.5);
    
    FragColor = vec4(color, 1.0);
}
