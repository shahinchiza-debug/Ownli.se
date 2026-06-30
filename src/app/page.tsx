'use client';

import { useState, useEffect, useRef } from 'react';
import {
  Globe, Mail, Shield, Smartphone, Clock, CheckCircle2, ArrowRight,
  Palette, BarChart3, MessageCircle, Server, UtensilsCrossed,
  Hammer, Heart, Scale, ShoppingCart, GraduationCap, Building, Sparkles,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import ShaderHero from '@/components/ShaderHero';
import OwnliLogo from '@/components/OwnliLogo';
import Navbar from '@/components/shared/Navbar';
import Footer from '@/components/shared/Footer';
import Link from 'next/link';
import Image from 'next/image';
import { Star } from 'lucide-react';

/* ─── Data ─── */
const industries = [
  { icon: UtensilsCrossed, name: 'Restaurang & café', desc: 'Online-meny, bordsbokning, catering' },
  { icon: Hammer, name: 'Hantverkare & bygg', desc: 'Portfolio, offerter, projektbilder' },
  { icon: Heart, name: 'Hälsa & vård', desc: 'Bokningssystem, personalpresentation' },
  { icon: Scale, name: 'Juridik & ekonomi', desc: 'Tjänstebeskrivningar, bokning' },
  { icon: ShoppingCart, name: 'Handel & e-handel', desc: 'Webbutik, produktkatalog' },
  { icon: GraduationCap, name: 'Utbildning', desc: 'Kurser, anmälan, CMS' },
  { icon: Building, name: 'Fastighet', desc: 'Objektlistning, kontaktformulär' },
  { icon: Sparkles, name: 'Friskvård & skönhet', desc: 'Bokning, galleri, behandlingar' },
];

const heroVariants: { title: [string, string, string]; subtitle: string }[] = [
  { title: ['Ditt företag förtjänar en ', 'fantastisk', ' hemsida'], subtitle: 'Sikta högre. Sikta mot stjärnorna.' },
  { title: ['Ditt företag förtjänar en hemsida som ', 'sticker ut', ''], subtitle: 'Varför nöja sig med mindre när ni kan sikta mot stjärnorna?' },
  { title: ['Ditt företag förtjänar ', 'mer', ' än bara en hemsida'], subtitle: 'Det förtjänar något som lyfter er mot stjärnorna.' },
  { title: ['En fantastisk hemsida för företag som vill ', 'högre', ''], subtitle: 'Sikta mot stjärnorna med en webbplats som verkligen syns.' },
  { title: ['Ditt företag förtjänar en ', 'fantastisk', ' hemsida'], subtitle: 'Bygg något större. Nå längre. Sikta mot stjärnorna.' },
];

const services = [
  { icon: Palette, title: 'Skräddarsydd design', desc: 'Unik och modern webbdesign anpassad efter ditt företags profil. Mobilanpassad, snabb och vacker.', img: '/images/card-build-presence.png' },
  { icon: Globe, title: '.SE-domän & hosting', desc: 'Vi ordnar din .SE-domän och lägger din hemsida på snabba och säkra servrar med 99.9% upptid.', img: '/images/card-succeed-online.png' },
  { icon: Mail, title: 'Professionell e-post', desc: 'info@dittforetag.se — e-post med SPF, DKIM och fullt spamskydd. Levereras varje gång.', img: '/images/card-hosting-easy.png' },
  { icon: Shield, title: 'SSL & säkerhet', desc: "Let's Encrypt SSL, Imunify360, ModSecurity WAF och dagliga backuper. Din hemsida är säker.", img: '/images/card-fast-secure.png' },
  { icon: Smartphone, title: 'Mobilanpassad', desc: '75% av dina besökare använder mobilen. Vi ser till att din hemsida ser fantastisk ut överallt.', img: '/images/card-site-priority.png' },
  { icon: BarChart3, title: 'SEO & statistik', desc: 'AWStats-trafikstatistik, Google-optimering och snabba laddningstider.', img: '/images/card-scalable.png' },
];

const testimonials = [
  { name: 'Marco Rossi', role: 'Ägare, Trattoria Bella', text: 'Våra gäster hittar oss enkelt och bordsbokningarna har ökat med 40% sedan vi bytte till Ownli. Fantastisk service!', stars: 5, img: '/images/testimonial1.jpg' },
  { name: 'Emma Lindqvist', role: 'Grundare, Nordbygg AB', text: 'Som entreprenör har jag ingen tid med teknik. Ownli sköter allt och deras support är fantastisk. Jag bara ringer och de fixar det.', stars: 5, img: '/images/testimonial2.jpg' },
  { name: 'Sara Ahmed', role: 'Klinikchef, Hälsokällan', text: 'Vårt bokningssystem online har revolutionerat vår verksamhet. Patienterna bokar enkelt dygnet runt — inga missade samtal längre.', stars: 5, img: '/images/testimonial3.jpg' },
];

/* ─── Scroll reveal hook ─── */
function useReveal(animateClass = 'reveal') {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const known = ['reveal', 'reveal-up-lg', 'reveal-left', 'reveal-right', 'reveal-scale', 'reveal-blur', 'reveal-clip', 'reveal-rotate', 'stagger-children', 'stagger-scale', 'process-stagger', 'stat-glow', 'line-draw', 'section-divider'];
    if (!known.some(c => el.classList.contains(c))) el.classList.add(animateClass);
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { el.classList.add('visible'); observer.unobserve(el); } },
      { threshold: 0.06, rootMargin: '0px 0px -32px 0px' }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);
  return ref;
}

/* ═══════════════════════════════════════════
   LANDING PAGE — Short & sweet, links to subpages
   ═══════════════════════════════════════════ */
function LandingPage() {
  const [isMobile, setIsMobile] = useState(false);
  const [heroIdx, setHeroIdx] = useState(0);
  useEffect(() => {
    setHeroIdx(Math.floor(Math.random() * heroVariants.length));
    setIsMobile(window.innerWidth < 768);
    const mq = window.matchMedia('(max-width: 767px)');
    const handler = (e: MediaQueryListEvent) => setIsMobile(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);
  const hero = heroVariants[heroIdx];

  const servicesRef = useReveal();
  const industriesRef = useReveal('reveal-blur');
  const industriesGridRef = useReveal();
  const ctaRef = useReveal();

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main id="main-content" className="flex-1">
        {/* HERO */}
        <section className="relative min-h-screen flex items-center overflow-hidden">
          {!isMobile ? (
            <ShaderHero className="bg-stone-950" />
          ) : (
            <div className="absolute inset-0 bg-gradient-to-br from-stone-950 via-blue-950 to-stone-950" />
          )}
          <div className="absolute inset-0 bg-gradient-to-r from-stone-950/80 via-stone-950/50 to-transparent pointer-events-none" />
          <div className="absolute inset-0 bg-gradient-to-t from-stone-950/70 via-transparent to-transparent pointer-events-none" />
          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 sm:py-40 w-full">
            <div className="max-w-2xl">
              <div className="mb-6 inline-flex items-center gap-2 text-blue-300 text-xs font-semibold tracking-[0.25em] uppercase font-[family-name:var(--font-display)] hero-badge-anim">
                <span className="h-px w-8 bg-blue-400/60" />Du äger. Vi bygger.<span className="h-px w-8 bg-blue-400/60" />
              </div>
              <h1 className="text-5xl sm:text-6xl lg:text-8xl font-extrabold text-white leading-[0.95] mb-6 font-[family-name:var(--font-display)]">
                <span className="hero-title-anim inline-block">{hero.title[0]}</span>
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300 hero-title-anim inline-block">{hero.title[1]}</span>
                <span className="hero-title-anim inline-block">{hero.title[2]}</span>
              </h1>
              <p className="text-lg sm:text-xl text-stone-300 mb-10 max-w-xl leading-relaxed hero-title-anim">{hero.subtitle}</p>
              <div className="flex flex-col sm:flex-row gap-4 hero-cta-anim">
                <Link href="/priser">
                  <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-8 text-lg h-14 w-full sm:w-auto shadow-lg shadow-blue-600/25 active:scale-[0.97] transition-transform">
                    Se våra priser <ArrowRight className="w-5 h-5 ml-2" />
                  </Button>
                </Link>
                <Link href="/tjanster">
                  <Button size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10 rounded-full px-8 text-lg h-14 w-full sm:w-auto active:scale-[0.97] transition-transform">
                    Våra tjänster
                  </Button>
                </Link>
              </div>
              <div className="mt-12 flex flex-wrap gap-2 sm:gap-3 hero-badges-anim">
                {['.SE-domän ingår', 'SSL/HTTPS inkluderat', 'Svensk support', '99.9% upptid'].map(l => (
                  <span key={l} className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/5 backdrop-blur-sm border border-white/10 text-stone-200 text-xs sm:text-sm">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />{l}
                  </span>
                ))}
              </div>
            </div>
          </div>
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
            <div className="w-6 h-10 rounded-full border-2 border-white/30 flex items-start justify-center pt-2">
              <div className="w-1.5 h-3 rounded-full bg-white/50" />
            </div>
          </div>
        </section>

        {/* SERVICES TEASER */}
        <section id="tjanster" className="py-24 sm:py-32 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-xl mb-16 reveal-up-lg" ref={servicesRef}>
              <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">Allt ditt företag behöver på nätet</h2>
              <p className="text-lg text-stone-500 leading-relaxed">Från domän och hosting till design och e-post — vi hanterar allt tekniskt så att du kan fokusera på din verksamhet.</p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8 stagger-scale" ref={useReveal()}>
              {services.map((s) => { const Icon = s.icon; return (
                <Card key={s.title} className="group relative border-stone-200 hover:border-stone-400 hover:shadow-xl transition-all duration-300 overflow-hidden">
                  <div className="absolute top-0 left-0 right-0 h-0.5 bg-blue-600 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left" />
                  {/* Service illustration */}
                  <div className="relative h-44 bg-gradient-to-br from-blue-50 to-stone-50 overflow-hidden">
                    <Image src={s.img} alt={s.title} fill className="object-cover object-center group-hover:scale-105 transition-transform duration-500" sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw" />
                    <div className="absolute inset-0 bg-gradient-to-t from-white via-transparent to-transparent" />
                  </div>
                  <CardHeader className="pb-2">
                    <div className="flex items-center gap-3 mb-1">
                      <div className="w-10 h-10 rounded-xl bg-stone-100 flex items-center justify-center group-hover:bg-blue-600 transition-all duration-300">
                        <Icon className="w-5 h-5 text-stone-700 group-hover:text-white transition-colors" />
                      </div>
                      <CardTitle className="text-lg text-stone-900 font-[family-name:var(--font-display)] flex items-center gap-2">
                        {s.title}
                        <ArrowRight className="w-4 h-4 text-stone-300 group-hover:text-blue-600 group-hover:translate-x-1 transition-all" />
                      </CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent><p className="text-stone-500 leading-relaxed text-sm">{s.desc}</p></CardContent>
                </Card>
              ); })}
            </div>
            <div className="mt-12 text-center">
              <Link href="/tjanster">
                <Button variant="outline" className="rounded-full border-stone-300 hover:border-stone-900 hover:bg-stone-900 hover:text-white transition-all px-8 h-12">
                  Se alla tjänster <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* INDUSTRIES */}
        <section id="branscher" className="py-24 sm:py-32 bg-stone-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16 reveal-blur" ref={industriesRef}>
              <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">Vi servar alla branscher</h2>
              <p className="text-lg text-stone-500">Oavsett bransch hjälper vi ditt företag att synas online</p>
            </div>
            <div className="flex lg:grid lg:grid-cols-4 gap-5 overflow-x-auto pb-4 lg:pb-0 snap-x snap-mandatory -mx-4 px-4 lg:mx-0 lg:px-0 scrollbar-hide stagger-scale" ref={industriesGridRef}>
              {industries.map(ind => { const Icon = ind.icon; return (
                <Card key={ind.name} className="group border-stone-200 hover:border-stone-400 hover:shadow-lg transition-all duration-300 text-center bg-white min-w-[200px] lg:min-w-0 snap-start shrink-0 lg:shrink">
                  <CardHeader className="items-center pb-2 pt-6">
                    <div className="w-14 h-14 rounded-2xl bg-stone-100 flex items-center justify-center mb-3 group-hover:bg-stone-900 group-hover:scale-110 transition-all duration-300">
                      <Icon className="w-7 h-7 text-stone-600 group-hover:text-white transition-colors" />
                    </div>
                    <CardTitle className="text-base font-semibold text-stone-900 font-[family-name:var(--font-display)]">{ind.name}</CardTitle>
                  </CardHeader>
                  <CardContent className="pb-6"><p className="text-stone-500 text-xs leading-relaxed">{ind.desc}</p></CardContent>
                </Card>
              ); })}
            </div>
          </div>
        </section>

        {/* PROCESS TEASER */}
        <section className="py-24 sm:py-32 bg-stone-900 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16 reveal-blur" ref={useReveal('reveal-blur')}>
              <h2 className="text-3xl sm:text-5xl font-bold mb-4 font-[family-name:var(--font-display)]">Fyra enkla steg</h2>
              <p className="text-lg text-stone-400">Från samtal till lansering. Vi gör det enkelt.</p>
            </div>
            <div className="relative grid sm:grid-cols-2 lg:grid-cols-4 gap-8 process-stagger" ref={useReveal()}>
              <div className="hidden lg:block absolute top-12 left-[12.5%] right-[12.5%] h-px bg-gradient-to-r from-transparent via-stone-700 to-transparent" />
              {[
                { n: '01', icon: MessageCircle, t: 'Vi pratar', d: 'Du berättar om ditt företag och vad du behöver.' },
                { n: '02', icon: Palette, t: 'Vi designar', d: 'Unik design som speglar din identitet.' },
                { n: '03', icon: Server, t: 'Vi bygger', d: 'Hemsida, domän, e-post, SSL och hosting.' },
                { n: '04', icon: Shield, t: 'Du äger', d: 'Full äganderätt — alltid.' },
              ].map(s => { const Icon = s.icon; return (
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
            <div className="mt-12 text-center">
              <Link href="/om-oss">
                <Button variant="outline" className="rounded-full border-white/30 text-white hover:bg-white/10 px-8 h-12 transition-all">
                  Läs mer om oss <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* CTA with image */}
        <section className="py-24 sm:py-32 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              <div className="reveal-left" ref={useReveal('reveal-left')}>
                <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-6 font-[family-name:var(--font-display)]">
                  Redo att <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-cyan-500">komma igång</span>?
                </h2>
                <p className="text-lg text-stone-500 mb-10 leading-relaxed">Välj mellan direktköp eller avbetalning. Du äger alltid din domän och din kod.</p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Link href="/priser">
                    <Button className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-8 h-12 text-base shadow-lg shadow-blue-600/25 active:scale-[0.97] transition-transform">
                      Se priser <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                  <Link href="/kontakt">
                    <Button variant="outline" className="rounded-full border-stone-300 hover:border-stone-900 hover:bg-stone-900 hover:text-white transition-all px-8 h-12">
                      Kontakta oss
                    </Button>
                  </Link>
                </div>
              </div>
              <div className="reveal-right" ref={useReveal('reveal-right')}>
                <div className="relative rounded-2xl overflow-hidden shadow-2xl shadow-stone-200/50 border border-stone-100">
                  <Image src="/images/features-grid.png" alt="Ownli — alla tjänster på ett ställe" width={1536} height={1024} className="w-full h-auto object-cover" />
                  <div className="absolute inset-0 bg-gradient-to-t from-stone-900/60 via-stone-900/10 to-transparent" />
                  <div className="absolute bottom-6 left-6 right-6">
                    <p className="text-white font-semibold text-lg font-[family-name:var(--font-display)]">Allt du behöver — på ett ställe</p>
                    <p className="text-stone-300 text-sm">Design, domän, hosting, e-post och säkerhet</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* TESTIMONIALS */}
        <section className="py-24 sm:py-32 bg-stone-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16 reveal-blur" ref={useReveal('reveal-blur')}>
              <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">Vad våra kunder säger</h2>
            </div>
            <div className="grid md:grid-cols-3 gap-8 stagger-scale" ref={useReveal()}>
              {testimonials.map(t => (
                <Card key={t.name} className="relative border-stone-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-white overflow-hidden">
                  <div className="absolute top-2 right-4 text-8xl leading-none text-stone-100 font-serif select-none pointer-events-none">&ldquo;</div>
                  <CardHeader className="pb-2 relative">
                    <div className="flex gap-0.5 mb-3">{Array.from({ length: t.stars }).map((_, i) => <Star key={i} className="w-4 h-4 fill-stone-800 text-stone-800" />)}</div>
                  </CardHeader>
                  <CardContent className="relative">
                    <p className="text-stone-700 leading-relaxed mb-6 text-[0.95rem]">&ldquo;{t.text}&rdquo;</p>
                    <div className="flex items-center gap-3 pt-4 border-t border-stone-100">
                      <div className="w-10 h-10 rounded-full overflow-hidden shrink-0 relative">
                        <Image src={t.img} alt={t.name} fill className="object-cover" sizes="40px" />
                      </div>
                      <div>
                        <p className="font-semibold text-stone-900 text-sm font-[family-name:var(--font-display)]">{t.name}</p>
                        <p className="text-xs text-stone-500">{t.role}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
      </main>

      <Footer />

      {/* MOBILE STICKY CTA */}
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

export default function Home() {
  return <LandingPage />;
}
