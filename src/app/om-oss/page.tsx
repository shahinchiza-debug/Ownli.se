'use client';

import { Shield, Globe, Headphones, Server, MessageCircle, Palette, ArrowRight } from 'lucide-react';
import Navbar from '@/components/shared/Navbar';
import Footer from '@/components/shared/Footer';
import { useReveal, useCounter } from '@/components/shared/hooks';
import Link from 'next/link';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { useRef, useState, useEffect } from 'react';

/* ── Stat counter component ── */
function StatCounter({ value, prefix = '', suffix = '', label }: { value: number; prefix?: string; suffix?: string; label: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const count = useCounter(visible ? value : 0, 1400);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.unobserve(el); } },
      { threshold: 0.3 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const display = value % 1 !== 0 ? count.toFixed(1) : count;

  return (
    <div ref={ref} className="space-y-1">
      <div className="text-4xl sm:text-5xl font-bold tracking-tight font-[family-name:var(--font-display)]">
        {prefix}{display}{suffix}
      </div>
      <div className="text-stone-500 text-sm font-medium">{label}</div>
    </div>
  );
}

const processSteps = [
  { n: '01', icon: MessageCircle, t: 'Vi pratar', d: 'Du berättar om ditt företag och vad du behöver. Vi lyssnar och ger råd.' },
  { n: '02', icon: Palette, t: 'Vi designar', d: 'Vi skapar en unik design som speglar ditt företags identitet. Du justerar tills du är nöjd.' },
  { n: '03', icon: Server, t: 'Vi bygger', d: 'Vi bygger din hemsida, ordnar .SE-domän, e-post, SSL och hosting. Allt driftklart.' },
  { n: '04', icon: Shield, t: 'Du äger', d: 'Vid direktköp äger du allt från dag 1. Vid avbetalning äger du allt när perioden är slut.' },
];

export default function OmOssPage() {
  const heroRef = useReveal();
  const storyRef = useReveal('reveal-left');
  const valuesRef = useReveal();
  const processRef = useReveal('reveal-blur');
  const processGridRef = useReveal();

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main id="main-content" className="flex-1 pt-20">
        {/* Hero */}
        <section className="py-16 sm:py-24 bg-gradient-to-b from-stone-50 to-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl reveal-up-lg" ref={heroRef}>
              <div className="mb-4 inline-flex items-center gap-2 text-blue-600 text-xs font-semibold tracking-[0.25em] uppercase font-[family-name:var(--font-display)]">
                <span className="h-px w-8 bg-blue-600/60" />Om oss<span className="h-px w-8 bg-blue-600/60" />
              </div>
              <h1 className="text-4xl sm:text-6xl font-bold text-stone-900 mb-6 font-[family-name:var(--font-display)]">
                Vi förstår <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-cyan-500">svenska företag</span> — och webben
              </h1>
              <p className="text-lg sm:text-xl text-stone-500 leading-relaxed">
                Ownli grundades med en enkel idé: svenska företag förtjänar bättre hemsidor. För ofta ser vi fantastiska företag med dåliga, långsamma eller osäkra hemsidor som kostar för mycket.
              </p>
            </div>
          </div>
        </section>

        {/* Our Story */}
        <section className="py-16 sm:py-24 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-5 gap-16 items-center">
              <div className="lg:col-span-3 reveal-left" ref={storyRef}>
                <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-8 font-[family-name:var(--font-display)]">Vår historia</h2>
                <div className="space-y-5 text-stone-500 leading-relaxed text-lg">
                  <p>Ownli grundades med en enkel idé: svenska företag förtjänar bättre hemsidor. För ofta ser vi fantastiska företag med dåliga, långsamma eller osäkra hemsidor som kostar för mycket. Det ska inte behöva vara så.</p>
                  <p>Vi kombinerar djup teknisk expertis inom WordPress, hosting och webbsäkerhet med en genuin förståelse för olika branschers unika behov. Oavsett om du driver en restaurang, ett byggföretag eller en advokatbyrå vet vi vad din hemsida behöver.</p>
                  <p>Vår filosofi är enkel: <strong className="text-stone-900">du äger din hemsida, din domän och din kod.</strong> Vi bygger åt dig, men du bestämmer. Det är därför vi kallar oss Ownli — för att du äger.</p>
                </div>
                <div className="mt-10 flex flex-wrap gap-8">
                  {[
                    { icon: Shield, t: 'Säker hosting', s: 'Imunify360 + WAF' },
                    { icon: Globe, t: '.SE-domäner', s: 'Certifierade registrarer' },
                    { icon: Headphones, t: 'Svensk support', s: 'Personlig & snabb' },
                  ].map(x => { const Icon = x.icon; return (
                    <div key={x.t} className="flex items-center gap-3">
                      <div className="w-11 h-11 rounded-lg bg-stone-100 flex items-center justify-center"><Icon className="w-5 h-5 text-stone-700" /></div>
                      <div><p className="font-semibold text-stone-900 text-sm font-[family-name:var(--font-display)]">{x.t}</p><p className="text-xs text-stone-500">{x.s}</p></div>
                    </div>
                  ); })}
                </div>
              </div>
              <div className="lg:col-span-2 relative reveal-right" ref={useReveal('reveal-right')}>
                <div className="aspect-[3/4] rounded-2xl overflow-hidden relative border border-stone-200 shadow-lg">
                  <Image src="/images/card-expert-support.png" alt="Ownli teamet" fill className="object-cover object-top" sizes="(max-width: 1024px) 100vw, 40vw" priority />
                  <div className="absolute inset-0 bg-gradient-to-t from-stone-900/80 via-stone-900/20 to-transparent" />
                  <div className="absolute bottom-6 left-6 right-6">
                    <p className="text-white font-semibold text-lg font-[family-name:var(--font-display)]">Teamet bakom Ownli</p>
                    <p className="text-stone-300 text-sm mt-1">Teknisk expertis & genuin omsorg</p>
                  </div>
                </div>
                <div className="absolute -bottom-6 -right-6 w-28 h-28 bg-stone-900 rounded-2xl flex items-center justify-center text-white shadow-xl shadow-stone-900/20">
                  <div className="text-center">
                    <div className="text-3xl font-bold font-[family-name:var(--font-display)]">5+</div>
                    <div className="text-xs text-stone-400">Års erfarenhet</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Infrastructure image full width */}
        <section className="py-16 sm:py-24 bg-stone-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="relative rounded-2xl overflow-hidden shadow-2xl shadow-stone-200/50" ref={valuesRef}>
              <div className="grid lg:grid-cols-2">
                <div className="relative aspect-[16/10] lg:aspect-auto">
                  <Image src="/images/card-succeed-online.png" alt="Serverinfrastruktur" fill className="object-cover" sizes="(max-width: 1024px) 100vw, 50vw" />
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent to-stone-50/10 lg:bg-gradient-to-r lg:from-transparent lg:to-stone-50" />
                </div>
                <div className="bg-stone-50 p-8 sm:p-12 flex flex-col justify-center">
                  <h3 className="text-2xl sm:text-3xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">Säker & snabb infrastruktur</h3>
                  <p className="text-stone-500 leading-relaxed mb-6">Våra servrar kör LiteSpeed-webbservern med CloudLinux för maximal stabilitet. Varje kundmiljö är isolerad, säker och optimerad för WordPress. Med Imunify360 och dagliga backuper sover du gott om natten.</p>
                  <Link href="/tjanster">
                    <Button variant="outline" className="rounded-full border-stone-300 hover:border-stone-900 hover:bg-stone-900 hover:text-white transition-all">
                      Läs om vår hosting <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Process */}
        <section className="py-16 sm:py-24 bg-stone-900 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16 reveal-blur" ref={processRef}>
              <h2 className="text-3xl sm:text-5xl font-bold mb-4 font-[family-name:var(--font-display)]">Fyra enkla steg</h2>
              <p className="text-lg text-stone-400">Från samtal till lansering. Vi gör det enkelt.</p>
            </div>
            <div className="relative grid sm:grid-cols-2 lg:grid-cols-4 gap-8 process-stagger" ref={processGridRef}>
              <div className="hidden lg:block absolute top-12 left-[12.5%] right-[12.5%] h-px bg-gradient-to-r from-transparent via-stone-700 to-transparent" />
              {processSteps.map(s => { const Icon = s.icon; return (
                <div key={s.n} className="relative text-center group">
                  <div className="relative inline-flex w-16 h-16 rounded-2xl bg-stone-800 ring-1 ring-stone-700 items-center justify-center mb-5 group-hover:bg-blue-600 group-hover:ring-blue-500 transition-all duration-300">
                    <Icon className="w-7 h-7 text-stone-400 group-hover:text-white transition-colors" />
                    <span className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-blue-600 text-white text-xs font-bold flex items-center justify-center ring-4 ring-stone-900 font-[family-name:var(--font-display)]">{s.n}</span>
                  </div>
                  <h3 className="text-xl font-bold mb-3 font-[family-name:var(--font-display)]">{s.t}</h3>
                  <p className="text-stone-400 leading-relaxed text-sm">{s.d}</p>
                </div>
              ); })}
            </div>
          </div>
        </section>

        {/* Stats */}
        <section className="relative py-14 bg-stone-950 overflow-hidden">
          <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, white 1px, transparent 0)', backgroundSize: '32px 32px' }} />
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center text-white stat-glow" ref={useReveal()}>
              <StatCounter value={99.9} suffix="%" label="Upptid" />
              <StatCounter value={2} prefix="< " suffix="s" label="Laddtid" />
              <StatCounter value={24} suffix="/7" label="Övervakning" />
              <StatCounter value={30} suffix=" dag" label="Backup-historik" />
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 sm:py-20 bg-white">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">Vill du veta mer?</h2>
            <p className="text-stone-500 text-lg mb-8">Läs om våra tjänster eller kontakta oss direkt för en kostnadsfri konsultation.</p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/tjanster">
                <Button variant="outline" className="rounded-full border-stone-300 hover:border-stone-900 px-8 h-12">
                  Våra tjänster
                </Button>
              </Link>
              <Link href="/kontakt">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-8 h-12 shadow-lg shadow-blue-600/25 active:scale-[0.97] transition-transform">
                  Kontakta oss <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />

      <div className="fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-t border-stone-200 p-3 lg:hidden safe-area-bottom">
        <Link href="/kontakt">
          <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-full h-12 text-base shadow-lg active:scale-[0.97] transition-transform">
            Kom igång <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </Link>
      </div>
    </div>
  );
}
