'use client';

import { useEffect, useRef } from 'react';

/**
 * ShaderHero — Animerad WebGL2 fragment shader som bakgrund.
 *
 * Visar flytande blåa moln med glödande former och musinteraktion.
 * Helt utan API — bara en <canvas> och GLSL-kod på GPU:n.
 *
 * Shader inspirerad av animated-shader-hero (ravikatiyar162),
 * anpassad för Ownli med djup blå palett (DEEP / MID / HIGHLIGHT).
 */

/* ─────────────────────────────────────────────────────────────
   SHADER-KÄLLKOD
   ───────────────────────────────────────────────────────────── */

const VERTEX_SHADER = `#version 300 es
in vec2 position;
void main() {
  gl_Position = vec4(position, 0.0, 1.0);
}`;

const FRAGMENT_SHADER = `#version 300 es
precision highp float;
out vec4 O;

uniform vec2  resolution;    // canvas-storlek i pixlar
uniform float time;          // tid i sekunder
uniform vec2  mouse;         // musposition i normaliserade koordinater [0..1]
uniform float mouseStrength; // hur mycket musen påverkar (0 = ingen, 1 = aktiv)

#define FC gl_FragCoord.xy
#define T  time
#define R  resolution
#define MN min(R.x, R.y)

// Pseudo-random för white noise
float rnd(vec2 p) {
  p = fract(p * vec2(12.9898, 78.233));
  p += dot(p, p + 34.56);
  return fract(p.x * p.y);
}

// Value noise (smooth interpolation av rnd)
float noise(in vec2 p) {
  vec2 i = floor(p), f = fract(p), u = f * f * (3.0 - 2.0 * f);
  float a = rnd(i),
        b = rnd(i + vec2(1.0, 0.0)),
        c = rnd(i + vec2(0.0, 1.0)),
        d = rnd(i + 1.0);
  return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

// Fractal Brownian Motion — flera oktaver av noise staplade på varandra
float fbm(vec2 p) {
  float t = 0.0, a = 1.0;
  mat2 m = mat2(1.0, -0.5, 0.2, 1.2);
  for (int i = 0; i < 5; i++) {
    t += a * noise(p);
    p *= 2.0 * m;
    a *= 0.5;
  }
  return t;
}

// Molnliknande fält
float clouds(vec2 p) {
  float d = 1.0, t = 0.0;
  for (float i = 0.0; i < 3.0; i++) {
    float a = d * fbm(i * 10.0 + p.x * 0.2 + 0.2 * (1.0 + i) * p.y + d + i * i + p);
    t = mix(t, d, a);
    d = a;
    p *= 2.0 / (i + 1.0);
  }
  return t;
}

// Blå palett: djup marin -> elektrisk blå -> cyan-topp
const vec3 DEEP      = vec3(0.02, 0.05, 0.18);   // djup marin
const vec3 MID       = vec3(0.10, 0.35, 0.85);   // elektrisk blå
const vec3 HIGHLIGHT = vec3(0.45, 0.80, 1.00);   // ljus cyan

void main(void) {
  vec2 uv = (FC - 0.5 * R) / MN;
  vec2 st = uv * vec2(2.0, 1.0);

  // Muspåverkan: skjuter UV-koordinaten lite åt musens håll
  vec2 mouseOffset = (mouse - 0.5) * mouseStrength * 0.4;
  st += mouseOffset;

  vec3 col = vec3(0.0);
  float bg = clouds(vec2(st.x + T * 0.5, -st.y));

  uv *= 1.0 - 0.3 * (sin(T * 0.2) * 0.5 + 0.5);

  // 12 lager av flytande, glödande former
  for (float i = 1.0; i < 12.0; i++) {
    uv += 0.1 * cos(i * vec2(0.1 + 0.01 * i, 0.8) + i * i + T * 0.5 + 0.1 * uv.x);
    vec2 p = uv;
    float d = length(p);

    // Modulera mellan blå toner
    vec3 glowTint = mix(MID, HIGHLIGHT, 0.5 + 0.5 * sin(i));
    col += 0.00125 / d * glowTint * (cos(sin(i) * vec3(1.0, 2.0, 3.0)) + 1.0);

    float b = noise(i + p + bg * 1.731);
    col += 0.002 * b / length(max(p, vec2(b * p.x * 0.02, p.y)));

    // Mixa mot djup marin i utkanten (där d är stor)
    vec3 bgColor = mix(DEEP, MID, bg);
    col = mix(col, bgColor, d);
  }

  // Subtil vignette för biokänsla
  float vignette = smoothstep(1.4, 0.3, length((FC - 0.5 * R) / MN));
  col *= 0.6 + 0.4 * vignette;

  // Ljusare cyan-toppskärning i mitten där intensiteten är hög
  float glow = clamp(max(col.b, col.g) - col.r, 0.0, 1.0);
  col += HIGHLIGHT * glow * 0.08;

  O = vec4(col, 1.0);
}`;

/* ─────────────────────────────────────────────────────────────
   REACT-KOMPONENT
   ───────────────────────────────────────────────────────────── */

interface ShaderHeroProps {
  /** Extra CSS-klasser för containern */
  className?: string;
  /** Lower resolution = better performance but more pixelated. Default 0.75. */
  resolutionScale?: number;
}

export default function ShaderHero({ className = '', resolutionScale = 0.75 }: ShaderHeroProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rafRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    /* --- 1. Skapa WebGL2-kontext --- */
    const gl = canvas.getContext('webgl2', {
      antialias: true,
      alpha: false,
      premultipliedAlpha: false,
    });
    if (!gl) {
      console.warn('WebGL2 stöds inte — ShaderHero faller tillbaka på statisk gradient.');
      return;
    }

    /* --- 2. Kompilera shaders --- */
    const compile = (type: number, src: string) => {
      const sh = gl.createShader(type);
      if (!sh) throw new Error('Kunde inte skapa shader');
      gl.shaderSource(sh, src);
      gl.compileShader(sh);
      if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
        const log = gl.getShaderInfoLog(sh);
        gl.deleteShader(sh);
        throw new Error('Shader-fel: ' + log);
      }
      return sh;
    };

    let program: WebGLProgram | null = null;
    try {
      const vs = compile(gl.VERTEX_SHADER, VERTEX_SHADER);
      const fs = compile(gl.FRAGMENT_SHADER, FRAGMENT_SHADER);
      program = gl.createProgram();
      if (!program) throw new Error('Kunde inte skapa program');
      gl.attachShader(program, vs);
      gl.attachShader(program, fs);
      gl.linkProgram(program);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        const log = gl.getProgramInfoLog(program);
        throw new Error('Program-länkningsfel: ' + log);
      }
      gl.deleteShader(vs);
      gl.deleteShader(fs);
    } catch (e) {
      console.error('ShaderHero:', e);
      return;
    }

    gl.useProgram(program);

    /* --- 3. Fullscreen quad (TRIANGLE_STRIP, 4 hörn) --- */
    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([
        -1,  1,
        -1, -1,
         1,  1,
         1, -1,
      ]),
      gl.STATIC_DRAW,
    );
    const posLoc = gl.getAttribLocation(program, 'position');
    gl.enableVertexAttribArray(posLoc);
    gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

    /* --- 4. Hämta uniforms --- */
    const uResolution    = gl.getUniformLocation(program, 'resolution');
    const uTime          = gl.getUniformLocation(program, 'time');
    const uMouse         = gl.getUniformLocation(program, 'mouse');
    const uMouseStrength = gl.getUniformLocation(program, 'mouseStrength');

    /* --- 5. Resize-hantering (DPR-medveten) --- */
    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = Math.max(1, Math.floor(window.innerWidth * dpr * resolutionScale));
      const h = Math.max(1, Math.floor(window.innerHeight * dpr * resolutionScale));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
        gl.viewport(0, 0, w, h);
      }
    };
    resize();
    window.addEventListener('resize', resize);

    /* --- 6. Musinteraktion (med mjuk easing) --- */
    let mouseX = 0.5, mouseY = 0.5;
    let targetMouseX = 0.5, targetMouseY = 0.5;
    let mouseStrength = 0;
    let targetStrength = 0;

    const onPointerMove = (e: PointerEvent) => {
      targetMouseX = e.clientX / window.innerWidth;
      targetMouseY = 1.0 - (e.clientY / window.innerHeight); // vänd Y för shader-koordinater
      targetStrength = 1.0;
    };
    const onPointerLeave = () => { targetStrength = 0; };

    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerleave', onPointerLeave);
    window.addEventListener('pointerout', onPointerLeave);

    /* --- 7. Animationsloop --- */
    const startTime = performance.now();
    const render = () => {
      // Mjuk interpolation mot målvärden
      mouseX        += (targetMouseX  - mouseX) * 0.06;
      mouseY        += (targetMouseY  - mouseY) * 0.06;
      mouseStrength += (targetStrength - mouseStrength) * 0.05;

      const t = (performance.now() - startTime) / 1000;

      gl.uniform2f(uResolution, canvas.width, canvas.height);
      gl.uniform1f(uTime, t);
      gl.uniform2f(uMouse, mouseX, mouseY);
      gl.uniform1f(uMouseStrength, mouseStrength);

      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      rafRef.current = requestAnimationFrame(render);
    };
    render();

    /* --- 8. Cleanup --- */
    return () => {
      cancelAnimationFrame(rafRef.current);
      window.removeEventListener('resize', resize);
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('pointerleave', onPointerLeave);
      window.removeEventListener('pointerout', onPointerLeave);
      if (buffer) gl.deleteBuffer(buffer);
      if (program) gl.deleteProgram(program);
    };
  }, [resolutionScale]);

  return (
    <canvas
      ref={canvasRef}
      className={`absolute inset-0 w-full h-full ${className}`}
      style={{ display: 'block' }}
      aria-hidden="true"
    />
  );
}
