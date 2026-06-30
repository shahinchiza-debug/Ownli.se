'use client';

import { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import OwnliLogo from '@/components/OwnliLogo';
import Link from 'next/link';

const navLinks = [
  { href: '/tjanster', label: 'Tjänster' },
  { href: '/om-oss', label: 'Om oss' },
  { href: '/priser', label: 'Priser' },
  { href: '/kontakt', label: 'Kontakt' },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const h = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', h);
    return () => window.removeEventListener('scroll', h);
  }, []);

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-md shadow-sm border-b border-stone-200' : 'bg-transparent'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">
          <Link href="/" className="flex items-center gap-2.5 group">
            <OwnliLogo size={36} markOnly />
            <span className="text-xl font-bold text-stone-900 group-hover:text-blue-700 transition-colors font-[family-name:var(--font-display)]">Ownli</span>
          </Link>
          <div className="hidden md:flex items-center gap-6">
            {navLinks.map(l => (
              <Link key={l.href} href={l.href} className="text-sm font-medium text-stone-600 hover:text-blue-700 transition-colors">
                {l.label}
              </Link>
            ))}
            <Link href="/kontakt">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-6 active:scale-[0.97] transition-transform">
                Kom igång
              </Button>
            </Link>
          </div>
          <button className="md:hidden p-2 text-stone-700" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Meny">
            {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>
      {mobileOpen && (
        <div className="md:hidden bg-white border-t border-stone-200 shadow-lg">
          <div className="px-4 py-4 space-y-3">
            {navLinks.map(l => (
              <Link key={l.href} href={l.href} className="block py-2 text-stone-700 font-medium hover:text-blue-700" onClick={() => setMobileOpen(false)}>
                {l.label}
              </Link>
            ))}
            <Link href="/kontakt" onClick={() => setMobileOpen(false)}>
              <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-full mt-2">Kom igång</Button>
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
