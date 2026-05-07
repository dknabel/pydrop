#version 330 core

uniform float iTime;
uniform vec2 iResolution;
uniform float iAmplitude;
uniform float iBass;
uniform float iMid;
uniform float iTreble;
uniform sampler1D iFrequency;

out vec4 FragColor;

vec3 julia(vec2 c, float maxiter) {
    vec2 z = c;
    float iter = 0.0;
    
    for(int i = 0; i < 100; i++) {
        if(length(z) > 2.0) break;
        z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
        iter += 1.0;
    }
    
    return vec3(iter / maxiter);
}

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= iResolution.x / iResolution.y;
    
    // Zoom and pan based on audio
    float zoom = 1.0 + iBass * 0.5;
    float pan = iTime * 0.1 + iMid * 2.0;
    
    uv /= zoom;
    uv += vec2(cos(pan), sin(pan)) * 0.5;
    
    // Julia set
    vec3 color = julia(uv, 256.0);
    
    // Add frequency coloring
    float freq = texture(iFrequency, fract(color.x)).r;
    color *= vec3(
        0.5 + 0.5 * sin(color.x * 3.0 + iTime),
        0.5 + 0.5 * sin(color.x * 3.0 + iTime + 2.0),
        0.5 + 0.5 * sin(color.x * 3.0 + iTime + 4.0)
    );
    
    color *= freq * (1.0 + iAmplitude);
    
    FragColor = vec4(color, 1.0);
}
