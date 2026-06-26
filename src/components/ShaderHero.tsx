'use client';

import { useEffect, useRef } from 'react';

/**
 * ShaderHero — Animerad WebGL2 fragment shader som bakgrund.
 * Visar rörande stjärnor/partiklar och rymd-moln.
 *
 * Shader hämtad från ravikatiyar162/animated-shader-hero och
 * anpassad för Ownli (amber/stone tema).
 */

const FRAGMENT_SHADER = `#version 300 es
precision highp float;
out vec4 O;
uniform vec2 resolution;
uniform float time;
#define FC gl_FragCoord.xy
#define T time
#define R resolution
#define MN min(R.x,R.y)

// Returns a pseudo random number for a given point (white noise)
float rnd(vec2 p) {
  p=fract(p*vec2(12.9898,78.233));
  p+=dot(p,p+34.56);
  return fract(p.x*p.y);
}
// Returns a pseudo random number for a given point (value noise)
float noise(in vec2 p) {
  vec2 i=floor(p), f=fract(p), u=f*f*(3.-2.*f);
  float a=rnd(i),
        b=rnd(i+vec2(1,0)),
        c=rnd(i+vec2(0,1)),
        d=rnd(i+1.);
  return mix(mix(a,b,u.x),mix(c,d,u.x),u.y);
}
// Returns a pseudo random number for a given point (fractal noise)
float fbm(vec2 p) {
  float t=.0, a=1.; mat2 m=mat2(1.,-.5,.2,1.2);
  for (int i=0; i<5; i++) {
    t+=a*noise(p);
    p*=2.*m;
    a*=.5;
  }
  return t;
}
float clouds(vec2 p) {
  float d=1., t=.0;
  for (float i=.0; i<3.; i++) {
    float a=d*fbm(i*10.+p.x*.2+.2*(1.+i)*p.y+d+i*i+p);
    t=mix(t,d,a);
    d=a;
    p*=2./(i+1.);
  }
  return t;
}
void main(void) {
  vec2 uv=(FC-.5*R)/MN,st=uv*vec2(2,1);
  vec3 col=vec3(0);
  float bg=clouds(vec2(st.x+T*.5,-st.y));
  uv*=1.-.3*(sin(T*.2)*.5+.5);
  for (float i=1.; i<12.; i++) {
    uv+=.1*cos(i*vec2(.1+.01*i, .8)+i*i+T*.5+.1*uv.x);
    vec2 p=uv;
    float d=length(p);
    // Stjärnor: blå-tonad (minskar rött, ökar blått)
    col+=.00125/d*(cos(sin(i)*vec3(1,2,3))+1.)*vec3(0.5, 0.8, 1.1);
    float b=noise(i+p+bg*1.731);
    col+=.002*b/length(max(p,vec2(b*p.x*.02,p.y)))*vec3(0.4, 0.7, 1.0);
    // Ownli blå-tema: kallt blått/ljusblått istället för varmt guld
    col=mix(col, vec3(bg*0.10, bg*0.45, bg*0.85), d);
  }
  O=vec4(col,1);
}`;

const VERTEX_SHADER = `#version 300 es
in vec2 a_position;
void main() {
  gl_Position = vec4(a_position, 0.0, 1.0);
}`;

interface ShaderHeroProps {
  /** Extra CSS-klasser för containern */
  className?: string;
  /** Lower resolution = better performance but more pixelated. Default 0.75. */
  resolutionScale?: number;
}

export default function ShaderHero({ className = '', resolutionScale = 0.75 }: ShaderHeroProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rafRef = useRef<number>(0);
  const glRef = useRef<WebGL2RenderingContext | null>(null);
  const programRef = useRef<WebGLProgram | null>(null);
  const uniformsRef = useRef<{ resolution: WebGLUniformLocation | null; time: WebGLUniformLocation | null }>({ resolution: null, time: null });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const gl = canvas.getContext('webgl2', { antialias: true, alpha: false, premultipliedAlpha: false });
    if (!gl) {
      console.warn('WebGL2 not supported — ShaderHero fallbacks to a static gradient.');
      return;
    }
    glRef.current = gl;

    // Kompilera shaders
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

    programRef.current = program;
    gl.useProgram(program);

    // Fullscreen quad
    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
    const posLoc = gl.getAttribLocation(program, 'a_position');
    gl.enableVertexAttribArray(posLoc);
    gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

    uniformsRef.current = {
      resolution: gl.getUniformLocation(program, 'resolution'),
      time: gl.getUniformLocation(program, 'time'),
    };

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

    const start = performance.now();
    const render = () => {
      const t = (performance.now() - start) / 1000;
      gl.uniform2f(uniformsRef.current.resolution, canvas.width, canvas.height);
      gl.uniform1f(uniformsRef.current.time, t);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
      rafRef.current = requestAnimationFrame(render);
    };
    render();

    return () => {
      cancelAnimationFrame(rafRef.current);
      window.removeEventListener('resize', resize);
      if (buffer) gl.deleteBuffer(buffer);
      if (program) gl.deleteProgram(program);
      glRef.current = null;
      programRef.current = null;
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
