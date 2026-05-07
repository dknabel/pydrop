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

    // Waveform line - highly responsive to amplitude
    float wave = abs(sin(uv.x * 10.0 - iTime) * 0.3) + freq * 0.5;
    float line = smoothstep(0.15, 0.0, abs(dist - freq * 1.5 - wave * iAmplitude * 2.0));

    // Color based on frequency - boost bass/mid/treble
    vec3 color = vec3(
        0.5 + 0.5 * sin(iTime + uv.x * 3.0 + iBass * 5.0),
        0.5 + 0.5 * sin(iTime + uv.y * 3.0 + 2.0 + iMid * 3.0),
        0.5 + 0.5 * sin(iTime + (uv.x + uv.y) * 3.0 + 4.0 + iTreble * 5.0)
    );

    // Boost audio reactivity significantly
    color *= (0.3 + iAmplitude * 1.5) * (1.0 + iBass);
    color += freq * vec3(1.0, 0.5, 0.2) * (1.0 + iAmplitude * 2.0);
    color += iBass * vec3(1.0, 0.3, 0.1) * 2.0;
    color += iTreble * vec3(0.1, 0.5, 1.0) * 2.0;

    FragColor = vec4(color * line, line);
}
