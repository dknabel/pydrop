#version 330 core

uniform float iTime;
uniform vec2 iResolution;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform sampler1D iFrequency;

out vec4 FragColor;

float plasma(vec2 p) {
    float x = sin(p.x * 0.5 + iTime * 0.3) * 0.5 + 0.5;
    float y = sin(p.y * 0.5 + iTime * 0.2) * 0.5 + 0.5;
    float z = sin((p.x + p.y) * 0.5 + iTime * 0.4) * 0.5 + 0.5;
    return x + y + z;
}

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    
    float freq = texture(iFrequency, uv.x).r;
    
    // Multiple plasma layers
    float p1 = plasma(uv * 3.0);
    float p2 = plasma(uv * 5.0 + vec2(iTime * 0.1));
    float p3 = plasma(uv * 7.0 - vec2(iTime * 0.15));
    
    float result = (p1 + p2 + p3) / 3.0;
    result *= freq * (1.0 + iAmplitude * 2.0);
    
    // Color gradient
    vec3 color = vec3(
        sin(result + iTime * 0.5) * 0.5 + 0.5,
        sin(result + iTime * 0.7 + 2.0) * 0.5 + 0.5,
        sin(result + iTime * 0.3 + 4.0) * 0.5 + 0.5
    );
    
    FragColor = vec4(color, result);
}
