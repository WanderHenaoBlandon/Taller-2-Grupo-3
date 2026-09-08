precision mediump float;

// GitHub: WanderHenaoBlandon

uniform vec2 u_resolution;

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution;
    vec2 p = uv - 0.5;
    p.x *= u_resolution.x / u_resolution.y;

    // Fondo blanco
    vec3 color = vec3(1.0);

    // Cara
    float face = length(p) - 0.3;
    if (face < 0.0) {
        color = vec3(1.0, 1.0, 0.0);
    }

    // Ojos
    float eye1 = length(p - vec2(-0.10, 0.08));
    float eye2 = length(p - vec2( 0.10, 0.08));

    if (eye1 < 0.03 || eye2 < 0.03) {
        color = vec3(0.0);
    }

    // Sonrisa
    float smile = abs(length(p - vec2(0.0, 0.0)) - 0.16);

    if (smile < 0.012 && p.y < 0.0) {
        color = vec3(0.0);
    }

    gl_FragColor = vec4(color, 1.0);
}