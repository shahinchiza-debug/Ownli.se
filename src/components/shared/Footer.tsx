'use client';

import OwnliLogo from '@/components/OwnliLogo';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-stone-900 text-stone-300 pt-16 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
          <div className="sm:col-span-2 lg:col-span-1">
            <Link href="/" className="flex items-center gap-2.5 mb-4">
              <OwnliLogo size={36} markOnly />
              <span className="text-xl font-bold text-white font-[family-name:var(--font-display)]">Ownli</span>
            </Link>
            <p className="text-sm leading-relaxed mb-5 text-stone-400">Professionella hemsidor för svenska företag. Design, hosting, domän och e-post — allt i ett.</p>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-stone-800 text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-stone-300">Alla system opererar normalt</span>
            </div>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4 text-sm font-[family-name:var(--font-display)]">Tjänster</h4>
            <ul className="space-y-2.5 text-sm">
              {[
                { label: 'Webbdesign', href: '/tjanster' },
                { label: 'WordPress', href: '/tjanster' },
                { label: '.SE-domän', href: '/tjanster' },
                { label: 'E-post', href: '/tjanster' },
                { label: 'Hosting', href: '/tjanster' },
              ].map(s => (
                <li key={s.label}>
                  <Link href={s.href} className="hover:text-white transition-colors">{s.label}</Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4 text-sm font-[family-name:var(--font-display)]">Företaget</h4>
            <ul className="space-y-2.5 text-sm">
              {[
                { label: 'Om oss', href: '/om-oss' },
                { label: 'Priser', href: '/priser' },
                { label: 'Kontakt', href: '/kontakt' },
              ].map(s => (
                <li key={s.label}>
                  <Link href={s.href} className="hover:text-white transition-colors">{s.label}</Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4 text-sm font-[family-name:var(--font-display)]">Legal</h4>
            <ul className="space-y-2.5 text-sm">
              {['Villkor', 'Integritetspolicy', 'Cookies'].map(s => (
                <li key={s}>
                  <span className="hover:text-white transition-colors cursor-pointer">{s}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div className="border-t border-stone-800 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm">
          <p className="text-stone-400">&copy; {new Date().getFullYear()} Ownli. Alla rättigheter förbehållna.</p>
          <p className="text-stone-500 text-xs">Du äger. Vi bygger. <span className="text-stone-700">·</span> Byggt i Sverige</p>
        </div>
      </div>
    </footer>
  );
}
