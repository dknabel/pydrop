#version 330 core

uniform float iTime;
uniform vec2 iResolution;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform sampler1D iFrequency;

out vec4 FragColor;

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    
    // Create Voronoi points
    vec2 cellSize = vec2(0.1 + iMid * 0.1);
    vec2 cellCoord = floor(uv / cellSize);
    vec2 cellUv = fract(uv / cellSize);
    
    float minDist = 1.0;
    vec3 cellColor = vec3(0.0);
    
    // Check 9 neighboring cells
    for(int x = -1; x <= 1; x++) {
        for(int y = -1; y <= 1; y++) {
            vec2 neighbor = cellCoord + vec2(x, y);
            float h = hash(neighbor);
            vec2 pointPos = fract(vec2(
                sin(h * 12.34) * 0.5 + 0.5,
                cos(h * 56.78) * 0.5 + 0.5
            ));
            
            // Add animation
            pointPos += vec2(sin(iTime * 0.5 + h), cos(iTime * 0.3 + h)) * 0.3;
            
            vec2 diff = cellUv - pointPos + vec2(x, y);
            float dist = length(diff);
            
            if(dist < minDist) {
                minDist = dist;
                cellColor = vec3(h, sin(h * 3.14 + iTime), cos(h * 3.14 + iTime)) * 0.5 + 0.5;
            }
        }
    }
    
    // Frequency response
    float freq = texture(iFrequency, hash(cellCoord)).r;
    cellColor *= freq * (1.0 + iAmplitude);
    
    // Edge detection
    float edge = smoothstep(0.05, 0.01, minDist);
    cellColor += edge * vec3(1.0) * iTreble;
    
    FragColor = vec4(cellColor, 1.0);
}
