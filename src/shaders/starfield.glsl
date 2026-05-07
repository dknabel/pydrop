#version 330 core

uniform float iTime;
uniform vec2 iResolution;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform sampler1D iFrequency;

out vec4 FragColor;

float hash(vec3 p) {
    return fract(sin(dot(p, vec3(12.9898, 78.233, 45.164))) * 43758.5453);
}

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= iResolution.x / iResolution.y;
    
    // 3D starfield
    vec3 dir = normalize(vec3(uv, 1.0));
    
    vec3 color = vec3(0.0);
    float speed = 0.5 + iBass;
    
    for(float i = 0.1; i < 1.0; i += 0.1) {
        vec3 pos = dir * i * 20.0;
        pos.z += iTime * speed;
        
        // Star positions
        vec3 cell = floor(pos);
        float h = hash(cell);
        
        // Star brightness
        float star = exp(-length(fract(pos) - 0.5) * 5.0) * h;
        star *= smoothstep(1.0, 0.0, i);
        
        // Color based on depth
        vec3 starColor = vec3(
            0.5 + 0.5 * sin(h * 3.14 + iTime * 0.5),
            0.5 + 0.5 * sin(h * 3.14 + iTime * 0.3 + 2.0),
            0.5 + 0.5 * sin(h * 3.14 + iTime * 0.7 + 4.0)
        );
        
        color += starColor * star * (1.0 + iAmplitude);
    }
    
    FragColor = vec4(color, 1.0);
}
