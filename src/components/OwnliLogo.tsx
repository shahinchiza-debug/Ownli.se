'use client';

/**
 * OwnliLogo — Varumärkesmark för Ownli ("Du äger. Vi bygger.").
 *
 * Designkoncept:
 * - En rounded square med blå gradient = "Vi bygger" (stabilitet, struktur).
 * - Inuti: en "O"-ring med en punkt i mitten = "Du äger" (keyhole, ägande).
 * - Kombinerar alltså varumärkets två löften i en enda minimalistisk mark.
 *
 * Marken är byggd i SVG och skalas linjärt med `size` (px). Fungerar
 * bra från favicon-storlek (16px) upp till dashboard-storlek (48px+).
 *
 * Färgerna är hårkodade till blå spektrumet så loggan är enhetlig
 * oavsett om den sitter på vit navbar, mörk hero eller stone-900 footer.
 */

interface OwnliLogoProps {
  /** Pixel-storlek (bredd = höjd). */
  size?: number;
  /** Visa bara logomarken utan ordmärket. */
  markOnly?: boolean;
  /** Ordmark-text ("Ownli" default). */
  wordmark?: string;
  /** Ordmark-klasser (färg etc). */
  wordmarkClassName?: string;
  /** Extra klasser på wrapper. */
  className?: string;
}

export default function OwnliLogo({
  size = 36,
  markOnly = false,
  wordmark = 'Ownli',
  wordmarkClassName = '',
  className = '',
}: OwnliLogoProps) {
  return (
    <span className={`inline-flex items-center gap-2.5 ${className}`}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 40 40"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
        className="shrink-0"
      >
        <defs>
          {/* Blå gradient — ljusare uppe till vänster, djupare nere till höger */}
          <linearGradient id="ownliLogoGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#60a5fa" />
            <stop offset="55%" stopColor="#3b82f6" />
            <stop offset="100%" stopColor="#1d4ed8" />
          </linearGradient>
          {/* Subtil inre glow för "punkt"-detaljen */}
          <radialGradient id="ownliLogoDot" cx="50%" cy="40%" r="60%">
            <stop offset="0%" stopColor="#ffffff" />
            <stop offset="100%" stopColor="#dbeafe" />
          </radialGradient>
        </defs>

        {/* Yttre rounded square — "Vi bygger" */}
        <rect width="40" height="40" rx="10" fill="url(#ownliLogoGrad)" />

        {/* O-ring — "Du äger" (ägarformen) */}
        <circle
          cx="20"
          cy="20"
          r="9"
          fill="none"
          stroke="white"
          strokeWidth="3"
          opacity="0.95"
        />

        {/* Keyhole-punkt i mitten — ägandet som låses */}
        <circle cx="20" cy="20" r="2.6" fill="url(#ownliLogoDot)" />
      </svg>

      {!markOnly && (
        <span className={wordmarkClassName}>{wordmark}</span>
      )}
    </span>
  );
}
