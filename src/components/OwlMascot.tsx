'use client';

import { useEffect, useState } from 'react';

/**
 * OwlMascot — Stiliserad animerad SVG-uggla.
 *
 * Designfilosofi:
 * - Geometriskt ren (cirkel/ellips-baserad) för att matcha Ownlis moderna varumärke
 * - Amber/guld-tema som kompletterar befintlig färgpalett
 * - Subtila animationer: blinkningar, huvudsvängningar, andning, vinge-rörelser
 * - Liten "surprise"-animation vid klick (ugglan blinkar snabbt + roterar huvudet)
 *
 * Ugglan symboliserar visdom, vaksamhet och skydd — perfekt för ett
 * varumärke som lovar "Du äger. Vi bygger."
 */

interface OwlMascotProps {
  /** Storlek i pixlar (bredd). Höjd beräknas automatiskt. */
  size?: number;
  /** Extra CSS-klasser */
  className?: string;
}

export default function OwlMascot({ size = 360, className = '' }: OwlMascotProps) {
  const [blinkKey, setBlinkKey] = useState(0);
  const [clicked, setClicked] = useState(false);

  // Slumpmässiga blinkningar var 3-6 sekund
  useEffect(() => {
    let timeout: ReturnType<typeof setTimeout>;
    const schedule = () => {
      const delay = 3000 + Math.random() * 3000;
      timeout = setTimeout(() => {
        setBlinkKey(k => k + 1);
        schedule();
      }, delay);
    };
    schedule();
    return () => clearTimeout(timeout);
  }, []);

  const handleClick = () => {
    setClicked(true);
    setBlinkKey(k => k + 1);
    setTimeout(() => setClicked(false), 1500);
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      aria-label="Ownli-ugglan (klicka för att säga hej)"
      className={`relative inline-block focus:outline-none ${className}`}
      style={{ width: size, height: size * 1.15, cursor: 'pointer' }}
    >
      <svg
        viewBox="0 0 360 420"
        width={size}
        height={size * 1.15}
        xmlns="http://www.w3.org/2000/svg"
        className="overflow-visible"
      >
        {/* Definitioner: gradients för kropp, ögon, näbb */}
        <defs>
          {/* Kropp – varmt guld/amber */}
          <radialGradient id="owlBody" cx="50%" cy="35%" r="70%">
            <stop offset="0%" stopColor="#fbbf24" />
            <stop offset="55%" stopColor="#d97706" />
            <stop offset="100%" stopColor="#78350f" />
          </radialGradient>
          {/* Mage – ljusare ton */}
          <radialGradient id="owlBelly" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#fef3c7" />
            <stop offset="70%" stopColor="#fcd34d" />
            <stop offset="100%" stopColor="#f59e0b" />
          </radialGradient>
          {/* Öga – djup bärnsten */}
          <radialGradient id="owlEye" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#fef3c7" />
            <stop offset="60%" stopColor="#fbbf24" />
            <stop offset="100%" stopColor="#92400e" />
          </radialGradient>
          {/* Gren – brun träton */}
          <linearGradient id="owlBranch" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#92400e" />
            <stop offset="100%" stopColor="#451a03" />
          </linearGradient>
          {/* Mjuk glöd bakom uggla */}
          <radialGradient id="owlGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="rgba(251, 191, 36, 0.35)" />
            <stop offset="60%" stopColor="rgba(217, 119, 6, 0.15)" />
            <stop offset="100%" stopColor="rgba(0, 0, 0, 0)" />
          </radialGradient>
        </defs>

        {/* Mjuk glöd */}
        <circle cx="180" cy="200" r="180" fill="url(#owlGlow)" />

        {/* Gren som ugglan sitter på */}
        <g className="owl-branch">
          <rect x="50" y="370" width="260" height="14" rx="7" fill="url(#owlBranch)" />
          {/* små kvistar */}
          <g fill="#451a03">
            <path d="M70 377 L40 365 L48 360 L75 372 Z" />
            <path d="M290 377 L320 365 L312 360 L285 372 Z" />
          </g>
        </g>

        {/* Hela uggla-gruppen med andnings-animation */}
        <g
          className="owl-body-group"
          style={{
            transformOrigin: '180px 290px',
            animation: 'owlBreathe 4s ease-in-out infinite',
          }}
        >
          {/* Vänster vinge */}
          <g
            style={{
              transformOrigin: '105px 240px',
              animation: 'owlWingLeft 6s ease-in-out infinite',
            }}
          >
            <path
              d="M105 200 Q 60 220, 50 280 Q 55 320, 95 310 Q 110 270, 115 230 Z"
              fill="#92400e"
              stroke="#451a03"
              strokeWidth="1.5"
            />
            {/* fjäderdetaljer */}
            <path d="M70 240 Q 80 250, 75 270" stroke="#451a03" strokeWidth="1" fill="none" />
            <path d="M65 270 Q 75 280, 70 300" stroke="#451a03" strokeWidth="1" fill="none" />
          </g>

          {/* Höger vinge */}
          <g
            style={{
              transformOrigin: '255px 240px',
              animation: 'owlWingRight 6s ease-in-out infinite',
            }}
          >
            <path
              d="M255 200 Q 300 220, 310 280 Q 305 320, 265 310 Q 250 270, 245 230 Z"
              fill="#92400e"
              stroke="#451a03"
              strokeWidth="1.5"
            />
            <path d="M290 240 Q 280 250, 285 270" stroke="#451a03" strokeWidth="1" fill="none" />
            <path d="M295 270 Q 285 280, 290 300" stroke="#451a03" strokeWidth="1" fill="none" />
          </g>

          {/* Kropp (äggform) */}
          <ellipse
            cx="180"
            cy="270"
            rx="105"
            ry="125"
            fill="url(#owlBody)"
            stroke="#451a03"
            strokeWidth="2"
          />

          {/* Mage (ljusare mittsektion) */}
          <ellipse
            cx="180"
            cy="295"
            rx="65"
            ry="85"
            fill="url(#owlBelly)"
            opacity="0.9"
          />

          {/* Mage-fjädertextur (små V:er) */}
          <g fill="#92400e" opacity="0.4">
            <path d="M155 270 L160 277 L165 270 Z" />
            <path d="M175 270 L180 277 L185 270 Z" />
            <path d="M195 270 L200 277 L205 270 Z" />
            <path d="M165 290 L170 297 L175 290 Z" />
            <path d="M185 290 L190 297 L195 290 Z" />
            <path d="M155 310 L160 317 L165 310 Z" />
            <path d="M175 310 L180 317 L185 310 Z" />
            <path d="M195 310 L200 317 L205 310 Z" />
            <path d="M165 330 L170 337 L175 330 Z" />
            <path d="M185 330 L190 337 L195 330 Z" />
          </g>

          {/* Tarser (fötter) syns under kroppen på grenen */}
          <g fill="#fbbf24" stroke="#92400e" strokeWidth="1.5">
            {/* vänster fot */}
            <ellipse cx="150" cy="368" rx="22" ry="8" />
            <path d="M132 368 L130 376 M150 368 L150 378 M168 368 L170 376" stroke="#92400e" strokeWidth="2" />
            {/* höger fot */}
            <ellipse cx="210" cy="368" rx="22" ry="8" />
            <path d="M192 368 L190 376 M210 368 L210 378 M228 368 L230 376" stroke="#92400e" strokeWidth="2" />
          </g>

          {/* Huvudgrupp med subtil svängning */}
          <g
            style={{
              transformOrigin: '180px 165px',
              animation: clicked
                ? 'owlHeadSpin 1.5s ease-in-out'
                : 'owlHeadSway 8s ease-in-out infinite',
            }}
          >
            {/* Örontofsar (fjädrar på huvudet) */}
            <path
              d="M105 90 L95 50 L130 80 Z"
              fill="#92400e"
              stroke="#451a03"
              strokeWidth="1.5"
            />
            <path
              d="M255 90 L265 50 L230 80 Z"
              fill="#92400e"
              stroke="#451a03"
              strokeWidth="1.5"
            />

            {/* Huvud (cirkel) */}
            <circle
              cx="180"
              cy="150"
              r="80"
              fill="url(#owlBody)"
              stroke="#451a03"
              strokeWidth="2"
            />

            {/* Ansiktsmask (ljusare hjärtform runt ögonen) */}
            <path
              d="M180 105
                 Q 130 100, 120 145
                 Q 115 180, 145 195
                 Q 165 205, 180 200
                 Q 195 205, 215 195
                 Q 245 180, 240 145
                 Q 230 100, 180 105 Z"
              fill="#fef3c7"
              opacity="0.95"
            />

            {/* Vänster öga */}
            <g key={`eyeL-${blinkKey}`}>
              <circle cx="150" cy="150" r="22" fill="url(#owlEye)" stroke="#451a03" strokeWidth="1.5" />
              {/* Pupil – animeras vid blink */}
              <g style={{ animation: 'owlBlink 0.4s ease-in-out' }}>
                <circle cx="150" cy="150" r="10" fill="#1c1917" />
                <circle cx="153" cy="147" r="3" fill="#fef3c7" opacity="0.9" />
              </g>
              {/* Ögonlock (animeras via CSS vid blink) */}
              <rect
                x="128" y="128" width="44" height="44"
                fill="url(#owlBody)"
                style={{
                  transformOrigin: '150px 150px',
                  animation: 'owlEyelid 0.18s ease-in-out',
                }}
              />
            </g>

            {/* Höger öga */}
            <g key={`eyeR-${blinkKey}`}>
              <circle cx="210" cy="150" r="22" fill="url(#owlEye)" stroke="#451a03" strokeWidth="1.5" />
              <g style={{ animation: 'owlBlink 0.4s ease-in-out' }}>
                <circle cx="210" cy="150" r="10" fill="#1c1917" />
                <circle cx="213" cy="147" r="3" fill="#fef3c7" opacity="0.9" />
              </g>
              <rect
                x="188" y="128" width="44" height="44"
                fill="url(#owlBody)"
                style={{
                  transformOrigin: '210px 150px',
                  animation: 'owlEyelid 0.18s ease-in-out',
                }}
              />
            </g>

            {/* Näbb */}
            <path
              d="M180 170 L168 188 L192 188 Z"
              fill="#f59e0b"
              stroke="#92400e"
              strokeWidth="1.5"
            />
            {/* Näbb-delning */}
            <line x1="180" y1="178" x2="180" y2="188" stroke="#92400e" strokeWidth="1" />
          </g>
        </g>

        {/* Subtila stjärnor runt uggla (dekorativa) */}
        <g fill="#fef3c7" opacity="0.6">
          <circle cx="40" cy="80" r="1.5">
            <animate attributeName="opacity" values="0.2;1;0.2" dur="3s" repeatCount="indefinite" />
          </circle>
          <circle cx="320" cy="120" r="2">
            <animate attributeName="opacity" values="1;0.3;1" dur="4s" repeatCount="indefinite" />
          </circle>
          <circle cx="20" cy="200" r="1">
            <animate attributeName="opacity" values="0.4;1;0.4" dur="2.5s" repeatCount="indefinite" />
          </circle>
          <circle cx="340" cy="220" r="1.5">
            <animate attributeName="opacity" values="1;0.4;1" dur="3.5s" repeatCount="indefinite" />
          </circle>
        </g>
      </svg>

      {/* Lokala keyframes – scoped via <style> så de laddas säkert */}
      <style>{`
        @keyframes owlBreathe {
          0%, 100% { transform: scale(1, 1); }
          50% { transform: scale(1.015, 0.985); }
        }
        @keyframes owlWingLeft {
          0%, 80%, 100% { transform: rotate(0deg); }
          85% { transform: rotate(-6deg); }
          90% { transform: rotate(2deg); }
          95% { transform: rotate(-3deg); }
        }
        @keyframes owlWingRight {
          0%, 80%, 100% { transform: rotate(0deg); }
          85% { transform: rotate(6deg); }
          90% { transform: rotate(-2deg); }
          95% { transform: rotate(3deg); }
        }
        @keyframes owlHeadSway {
          0%, 100% { transform: rotate(0deg); }
          25% { transform: rotate(-3deg); }
          75% { transform: rotate(3deg); }
        }
        @keyframes owlHeadSpin {
          0% { transform: rotate(0deg); }
          30% { transform: rotate(15deg); }
          60% { transform: rotate(-15deg); }
          100% { transform: rotate(0deg); }
        }
        @keyframes owlBlink {
          0%, 100% { transform: scaleY(1); }
          50% { transform: scaleY(0.1); }
        }
        @keyframes owlEyelid {
          0% { transform: scaleY(0); }
          50% { transform: scaleY(1); }
          100% { transform: scaleY(0); }
        }
      `}</style>
    </button>
  );
}
