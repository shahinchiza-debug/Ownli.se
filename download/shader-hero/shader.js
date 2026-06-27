/* =========================================================================
   WEBGL2 SHADER HERO
   - Ingen React, ingen Vite, ingen API, inga npm-beroenden
   - Bara en HTML-fil + CSS + denna JS-fil som körs direkt i webbläsaren
   ========================================================================= */

(function () {
  "use strict";

  // ----------------------------------------------------------------
  // 1. Hämta canvas och skapa WebGL2-kontext
  // ----------------------------------------------------------------
  const canvas = document.getElementById("shader-canvas");
  const gl = canvas.getContext("webgl2", { antialias: true, premultipliedAlpha: false });

  if (!gl) {
    document.body.innerHTML =
      "<p style='color:#fff;font-family:sans-serif;padding:2rem'>Din webbläsare stöder inte WebGL2.</p>";
    return;
  }

  // ----------------------------------------------------------------
  // 2. Vertex shader: ritar en "full-screen quad" (två trianglar som täcker hela skärmen)
  // ----------------------------------------------------------------
  const vertexSrc = `#version 300 es
  in vec2 position;
  void main() {
    gl_Position = vec4(position, 0.0, 1.0);
  }`;

  // ----------------------------------------------------------------
  // 3. Fragment shader: HJÄRTAT av animationen
  //    Körs en gång per pixel på GPU:n
  // ----------------------------------------------------------------
  const fragmentSrc = `#version 300 es
  precision highp float;
  out vec4 O;

  uniform vec2  resolution;    // canvas-storlek i pixlar
  uniform float time;          // tid i sekunder
  uniform vec2  mouse;         // musposition i normaliserade koordinater
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
          b = rnd(i + vec2(1, 0)),
          c = rnd(i + vec2(0, 1)),
          d = rnd(i + 1.0);
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
  }

  // Fractal Brownian Motion - flera oktaver av noise staplade på varandra
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

    // Subtil vignette-rungen för biokänsla
    float vignette = smoothstep(1.4, 0.3, length((FC - 0.5 * R) / MN));
    col *= 0.6 + 0.4 * vignette;

    // Ljusare cyan-toppskärning i mitten där intensiteten är hög
    float glow = clamp(max(col.b, col.g) - col.r, 0.0, 1.0);
    col += HIGHLIGHT * glow * 0.08;

    O = vec4(col, 1.0);
  }`;

  // ----------------------------------------------------------------
  // 4. Hjälpfunktion: kompilera shader med felhantering
  // ----------------------------------------------------------------
  function compileShader(type, source) {
    const sh = gl.createShader(type);
    gl.shaderSource(sh, source);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      console.error("Shader-fel:", gl.getShaderInfoLog(sh));
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }

  // ----------------------------------------------------------------
  // 5. Bygg program: vertex + fragment -> linkat program
  // ----------------------------------------------------------------
  const vs = compileShader(gl.VERTEX_SHADER, vertexSrc);
  const fs = compileShader(gl.FRAGMENT_SHADER, fragmentSrc);
  const program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error("Link-fel:", gl.getProgramInfoLog(program));
    return;
  }
  gl.useProgram(program);

  // ----------------------------------------------------------------
  // 6. Full-screen quad: två trianglar som täcker hela skärmen
  // ----------------------------------------------------------------
  const vertices = new Float32Array([
    -1,  1,
    -1, -1,
     1,  1,
     1, -1
  ]);
  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
  const posLoc = gl.getAttribLocation(program, "position");
  gl.enableVertexAttribArray(posLoc);
  gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

  // ----------------------------------------------------------------
  // 7. Hämta uniforms (variabler vi skickar in till shadern varje frame)
  // ----------------------------------------------------------------
  const uResolution    = gl.getUniformLocation(program, "resolution");
  const uTime          = gl.getUniformLocation(program, "time");
  const uMouse         = gl.getUniformLocation(program, "mouse");
  const uMouseStrength = gl.getUniformLocation(program, "mouseStrength");

  // ----------------------------------------------------------------
  // 8. Resize-hantering (DPR-medveten)
  // ----------------------------------------------------------------
  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = window.innerWidth  * dpr;
    const h = window.innerHeight * dpr;
    canvas.width  = w;
    canvas.height = h;
    canvas.style.width  = window.innerWidth  + "px";
    canvas.style.height = window.innerHeight + "px";
    gl.viewport(0, 0, w, h);
  }
  window.addEventListener("resize", resize);
  resize();

  // ----------------------------------------------------------------
  // 9. Musinteraktion
  // ----------------------------------------------------------------
  let mouseX = 0.5, mouseY = 0.5;
  let targetMouseX = 0.5, targetMouseY = 0.5;
  let mouseStrength = 0;
  let targetStrength = 0;

  window.addEventListener("pointermove", (e) => {
    targetMouseX = e.clientX / window.innerWidth;
    targetMouseY = 1.0 - (e.clientY / window.innerHeight); // vänd Y för shader-koordinater
    targetStrength = 1.0;
  });
  window.addEventListener("pointerleave", () => { targetStrength = 0; });
  window.addEventListener("pointerout",   () => { targetStrength = 0; });

  // ----------------------------------------------------------------
  // 10. Animationsloop
  // ----------------------------------------------------------------
  const startTime = performance.now();
  function frame() {
    // Mjukt interpolation mot målvärden (easing)
    mouseX        += (targetMouseX     - mouseX)     * 0.06;
    mouseY        += (targetMouseY     - mouseY)     * 0.06;
    mouseStrength += (targetStrength - mouseStrength) * 0.05;

    const t = (performance.now() - startTime) * 0.001;

    gl.uniform2f(uResolution,    canvas.width, canvas.height);
    gl.uniform1f(uTime,          t);
    gl.uniform2f(uMouse,         mouseX, mouseY);
    gl.uniform1f(uMouseStrength, mouseStrength);

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    requestAnimationFrame(frame);
  }
  frame();
})();
