'use client';

import { useState, useEffect, useRef } from 'react';
import {
  Globe, Mail, Shield, Smartphone, Clock, CheckCircle2, ArrowRight,
  Menu, X, ChevronRight, Star, UtensilsCrossed, Server, Palette, Search,
  MessageCircle, BarChart3, Headphones, Hammer, Heart, Scale, ShoppingCart,
  GraduationCap, Building, Sparkles,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import ShaderHero from '@/components/ShaderHero';
import OwnliLogo from '@/components/OwnliLogo';

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

const purchaseOptions = [
  { name: 'Direktköp', price: '35 000', unit: 'kr', desc: 'Kunden köper hemsidan direkt och äger den fullt ut från dag ett.', features: ['Full äganderätt från dag 1', 'Drift och hosting väljs fritt', 'Ingen bindningstid', 'All kod och material tillhör dig', 'Fri att flytta när du vill'], highlighted: false },
  { name: 'Avbetalning 2 år', price: '2 000', unit: 'kr/månaden', desc: 'Hemsidan betalas av under 24 månader, varefter full äganderätt övergår till kunden.', features: ['Betalning över 24 månader', 'Hosting, drift och support ingår', '1 större omfaktorering ingår', 'Full äganderätt efter perioden', 'Välj driftpartner fritt efteråt'], highlighted: true },
];

/* Hero-varianter: [före, markera, efter] + underrubrik. */
const heroVariants: { title: [string, string, string]; subtitle: string }[] = [
  { title: ['Ditt företag förtjänar en ', 'fantastisk', ' hemsida'], subtitle: 'Sikta högre. Sikta mot stjärnorna.' },
  { title: ['Ditt företag förtjänar en hemsida som ', 'sticker ut', ''], subtitle: 'Varför nöja sig med mindre när ni kan sikta mot stjärnorna?' },
  { title: ['Ditt företag förtjänar ', 'mer', ' än bara en hemsida'], subtitle: 'Det förtjänar något som lyfter er mot stjärnorna.' },
  { title: ['En fantastisk hemsida för företag som vill ', 'högre', ''], subtitle: 'Sikta mot stjärnorna med en webbplats som verkligen syns.' },
  { title: ['Ditt företag förtjänar en ', 'fantastisk', ' hemsida'], subtitle: 'Bygg något större. Nå längre. Sikta mot stjärnorna.' },
];

const services = [
  { icon: Palette, title: 'Skräddarsydd design', desc: 'Unik och modern webbdesign anpassad efter ditt företags profil och varumärke. Mobilanpassad, snabb och vacker — varje gång.' },
  { icon: Globe, title: '.SE-domän & hosting', desc: 'Vi ordnar din .SE-domän och lägger din hemsida på snabba och säkra servrar med 99.9% upptid. WHM/cPanel för professionell drift.' },
  { icon: Mail, title: 'Professionell e-post', desc: 'info@dittforetag.se, kontakt@dittforetag.se — e-post med SPF, DKIM och fullt spamskydd. Levereras varje gång.' },
  { icon: Shield, title: 'SSL & säkerhet', desc: "Let's Encrypt SSL-certifikat, Imunify360 antivirusskydd, ModSecurity WAF och dagliga backuper. Din hemsida är säker hos oss." },
  { icon: Smartphone, title: 'Mobilanpassad', desc: '75% av dina besökare använder mobilen. Vi ser till att din hemsida ser fantastisk ut på alla skärmstorlekar — telefon, surfplatta och dator.' },
  { icon: BarChart3, title: 'SEO & statistik', desc: 'AWStats-trafikstatistik, Google-optimering och snabba laddningstider. Så att nya kunder hittar ditt företag på nätet.' },
];

const testimonials = [
  { name: 'Marco Rossi', role: 'Ägare, Trattoria Bella', text: 'Våra gäster hittar oss enkelt och bordsbokningarna har ökat med 40% sedan vi bytte till Ownli. Fantastisk service!', stars: 5 },
  { name: 'Emma Lindqvist', role: 'Grundare, Nordbygg AB', text: 'Som entreprenör har jag ingen tid med teknik. Ownli sköter allt och deras support är fantastisk. Jag bara ringer och de fixar det.', stars: 5 },
  { name: 'Sara Ahmed', role: 'Klinikchef, Hälsokällan', text: 'Vårt bokningssystem online har revolutionerat vår verksamhet. Patienterna bokar enkelt dygnet runt — inga missade samtal längre.', stars: 5 },
];

const faqs = [
  { q: 'Vad är skillnaden mellan direktköp och avbetalning?', a: 'Vid direktköp betalar du 35 000 kr och äger hemsidan från dag ett — du väljer själv hosting och drift. Vid avbetalning betalar du 2 000 kr per månad i 24 månader — under perioden ingår hosting, support och en större omfaktorering. Efter 24 månaderna övergår full äganderätt till dig.' },
  { q: 'Vad händer efter avbetalningen är klar?', a: 'När de 24 månaderna är slut äger du hemsidan fullt ut. Du väljer då fritt om du vill ha kvar oss som driftpartner, ta över hosting på egen hand, eller flytta till en annan leverantör. Det är ditt val.' },
  { q: 'Ingår hosting i priset?', a: 'Direktköp (35 000 kr) är själva hemsidan — du väljer därefter hosting själv eller via oss. Vid avbetalning under 24 månader ingår drift, support och uppdateringar under hela perioden.' },
  { q: 'Vad händer med min domän om jag vill flytta?', a: 'Du äger alltid din domän. Vill du flytta till en annan leverantör hjälper vi dig kostnadsfritt att överföra den, oavsett om du köpt direkt eller via avbetalning.' },
  { q: 'Kan ni uppdatera hemsidan senare?', a: 'Ja. Mindre justeringar och större omfaktoreringar tar vi per uppdrag. Du får alltid en fast prisuppskattning i förväg så att du vet vad som gäller.' },
  { q: 'Kan jag flytta min befintliga hemsida till er?', a: 'Absolut! Vi migrerar din befintliga WordPress-hemsida utan driftavbrott. Kontakta oss så löser vi övergången smidigt.' },
  { q: 'Vilka branscher servar ni?', a: 'Alla! Från restauranger och hantverkare till juridik och e-handel. Vi anpassar varje hemsida efter er bransch och era behov.' },
];

/* ─── Scroll reveal hook ─── */
function useReveal() {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { el.classList.add('visible'); observer.unobserve(el); } },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);
  return ref;
}

/* ═══════════════════════════════════════════
   LANDING PAGE
   ═══════════════════════════════════════════ */
function LandingPage() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [faqOpen, setFaqOpen] = useState<number | null>(null);
  const [contactSent, setContactSent] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  // Slumpa hero-variant först på klienten (efter montering).
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

  useEffect(() => {
    const h = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', h);
    return () => window.removeEventListener('scroll', h);
  }, []);

  const navLinks = [
    { href: '#tjanster', label: 'Tjänster' }, { href: '#branscher', label: 'Branscher' },
    { href: '#priser', label: 'Priser' }, { href: '#process', label: 'Process' },
    { href: '#om-oss', label: 'Om oss' }, { href: '#kontakt', label: 'Kontakt' },
  ];

  const handleContact = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    try {
      await fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: fd.get('name'), email: fd.get('email'), phone: fd.get('phone'), company: fd.get('company'), message: fd.get('message') }) });
      setContactSent(true);
      setTimeout(() => setContactSent(false), 4000);
      (e.target as HTMLFormElement).reset();
    } catch { /* silent */ }
  };

  // Scroll reveal refs
  const servicesRef = useReveal();
  const industriesRef = useReveal();
  const pricingRef = useReveal();
  const processRef = useReveal();
  const testimonialsRef = useReveal();
  const aboutRef = useReveal();
  const faqRef = useReveal();
  const contactRef = useReveal();

  return (
    <div className="min-h-screen flex flex-col">
      {/* NAVBAR */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-md shadow-sm border-b border-stone-200' : 'bg-transparent'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 sm:h-20">
            <a href="#" className="flex items-center gap-2.5 group">
              <OwnliLogo size={36} markOnly />
              <span className="text-xl font-bold text-stone-900 group-hover:text-blue-700 transition-colors font-[family-name:var(--font-display)]">Ownli</span>
            </a>
            <div className="hidden md:flex items-center gap-6">
              {navLinks.map(l => <a key={l.href} href={l.href} className="text-sm font-medium text-stone-600 hover:text-blue-700 transition-colors">{l.label}</a>)}
              <a href="#kontakt"><Button className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-6 active:scale-[0.97] transition-transform">Kom igång</Button></a>
            </div>
            <button className="md:hidden p-2 text-stone-700" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Meny">
              {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
        {mobileOpen && (
          <div className="md:hidden bg-white border-t border-stone-200 shadow-lg">
            <div className="px-4 py-4 space-y-3">
              {navLinks.map(l => <a key={l.href} href={l.href} className="block py-2 text-stone-700 font-medium hover:text-blue-700" onClick={() => setMobileOpen(false)}>{l.label}</a>)}
              <a href="#kontakt" onClick={() => setMobileOpen(false)}><Button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-full mt-2">Kom igång</Button></a>
            </div>
          </div>
        )}
      </nav>

      <main id="main-content" className="flex-1">
        {/* HERO — Asymmetric: text left, shader bleeds right */}
        <section className="relative min-h-screen flex items-center overflow-hidden">
          {/* Shader as full background */}
          {!isMobile ? (
            <ShaderHero className="bg-stone-950" />
          ) : (
            <div className="absolute inset-0 bg-gradient-to-br from-stone-950 via-blue-950 to-stone-950" />
          )}
          <div className="absolute inset-0 bg-gradient-to-r from-stone-950/80 via-stone-950/50 to-transparent pointer-events-none" />
          <div className="absolute inset-0 bg-gradient-to-t from-stone-950/70 via-transparent to-transparent pointer-events-none" />
          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 sm:py-40 w-full">
            {/* LEFT-ALIGNED hero for character */}
            <div className="max-w-2xl">
              <div className="mb-6 inline-flex items-center gap-2 text-blue-300 text-xs font-semibold tracking-[0.25em] uppercase font-[family-name:var(--font-display)]"><span className="h-px w-8 bg-blue-400/60" />Du äger. Vi bygger.<span className="h-px w-8 bg-blue-400/60" /></div>
              <h1 className="text-5xl sm:text-6xl lg:text-8xl font-extrabold text-white leading-[0.95] mb-6 font-[family-name:var(--font-display)]">{hero.title[0]}<span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">{hero.title[1]}</span>{hero.title[2]}</h1>
              <p className="text-lg sm:text-xl text-stone-300 mb-10 max-w-xl leading-relaxed">{hero.subtitle}</p>
              <div className="flex flex-col sm:flex-row gap-4">
                <a href="#priser"><Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-8 text-lg h-14 w-full sm:w-auto shadow-lg shadow-blue-600/25 active:scale-[0.97] transition-transform">Se våra priser <ArrowRight className="w-5 h-5 ml-2" /></Button></a>
                <a href="#process"><Button size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10 rounded-full px-8 text-lg h-14 w-full sm:w-auto active:scale-[0.97] transition-transform">Så fungerar det</Button></a>
              </div>
              <div className="mt-12 flex flex-wrap gap-2 sm:gap-3">
                {['.SE-domän ingår', 'SSL/HTTPS inkluderat', 'Svensk support', '99.9% upptid'].map(l => (
                  <span key={l} className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/5 backdrop-blur-sm border border-white/10 text-stone-200 text-xs sm:text-sm">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />{l}
                  </span>
                ))}
              </div>
            </div>
          </div>
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce"><div className="w-6 h-10 rounded-full border-2 border-white/30 flex items-start justify-center pt-2"><div className="w-1.5 h-3 rounded-full bg-white/50" /></div></div>
        </section>

        {/* SERVICES — 2+1 asymmetric grid */}
        <section id="tjanster" className="py-24 sm:py-32 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-xl mb-16 reveal" ref={servicesRef}>
              <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">Allt ditt företag behöver på nätet</h2>
              <p className="text-lg text-stone-500 leading-relaxed">Från domän och hosting till design och e-post — vi hanterar allt tekniskt så att du kan fokusera på din verksamhet.</p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
              {services.map((s, i) => { const Icon = s.icon; return (
                <Card key={s.title} className={`group relative border-stone-200 hover:border-stone-400 hover:shadow-lg transition-all duration-300 overflow-hidden ${i === 0 ? 'sm:col-span-2 lg:col-span-1' : ''}`}>
                  <div className="absolute top-0 left-0 right-0 h-0.5 bg-stone-900 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left" />
                  <CardHeader>
                    <div className="w-12 h-12 rounded-xl bg-stone-100 flex items-center justify-center mb-3 group-hover:bg-stone-900 transition-all duration-300">
                      <Icon className="w-6 h-6 text-stone-700 group-hover:text-white transition-colors" />
                    </div>
                    <CardTitle className="text-xl text-stone-900 font-[family-name:var(--font-display)] flex items-center justify-between gap-2">
                      {s.title}
                      <ArrowRight className="w-4 h-4 text-stone-300 group-hover:text-stone-900 group-hover:translate-x-1 transition-all" />
                    </CardTitle>
                  </CardHeader>
                  <CardContent><p className="text-stone-500 leading-relaxed text-sm">{s.desc}</p></CardContent>
                </Card>); })}
            </div>
          </div>
        </section>

        {/* INDUSTRIES — Horizontal scroll on mobile */}
        <section id="branscher" className="py-24 sm:py-32 bg-stone-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16 reveal" ref={industriesRef}>
              <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">Vi servar alla branscher</h2>
              <p className="text-lg text-stone-500">Oavsett bransch hjälper vi ditt företag att synas online</p>
            </div>
            {/* Mobile: horizontal scroll. Desktop: grid */}
            <div className="flex lg:grid lg:grid-cols-4 gap-5 overflow-x-auto pb-4 lg:pb-0 snap-x snap-mandatory -mx-4 px-4 lg:mx-0 lg:px-0 scrollbar-hide">
              {industries.map(ind => { const Icon = ind.icon; return (
                <Card key={ind.name} className="group border-stone-200 hover:border-stone-400 hover:shadow-lg transition-all duration-300 text-center bg-white min-w-[200px] lg:min-w-0 snap-start shrink-0 lg:shrink">
                  <CardHeader className="items-center pb-2 pt-6">
                    <div className="w-14 h-14 rounded-2xl bg-stone-100 flex items-center justify-center mb-3 group-hover:bg-stone-900 group-hover:scale-110 transition-all duration-300">
                      <Icon className="w-7 h-7 text-stone-600 group-hover:text-white transition-colors" />
                    </div>
                    <CardTitle className="text-base font-semibold text-stone-900 font-[family-name:var(--font-display)]">{ind.name}</CardTitle>
                  </CardHeader>
                  <CardContent className="pb-6"><p className="text-stone-500 text-xs leading-relaxed">{ind.desc}</p></CardContent>
                </Card>); })}
            </div>
          </div>
        </section>

        {/* PRICING — Clean with breathing room */}
        <section id="priser" className="py-24 sm:py-32 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16 reveal" ref={pricingRef}>
              <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">Transparenta priser</h2>
              <p className="text-lg text-stone-500">Du äger, vi bygger. Alla priser exkl. moms.</p>
            </div>

            <div className="mb-20">
              <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                {purchaseOptions.map(opt => (
                  <Card key={opt.name} className={`relative flex flex-col transition-all duration-300 hover:-translate-y-1 ${opt.highlighted ? 'border-2 border-blue-600 shadow-xl shadow-blue-500/10 scale-[1.02] bg-gradient-to-b from-blue-50/50 to-white' : 'border-stone-200 hover:shadow-lg hover:border-stone-300'}`}>
                    {opt.highlighted && <div className="absolute -top-4 left-1/2 -translate-x-1/2"><Badge className="bg-blue-600 text-white px-4 py-1 text-sm shadow-md shadow-blue-600/30">Mest populär</Badge></div>}
                    <CardHeader className="pb-2 pt-6">
                      <CardTitle className="text-2xl text-stone-900 font-[family-name:var(--font-display)]">{opt.name}</CardTitle>
                      <p className="text-stone-500 text-sm leading-relaxed pt-1">{opt.desc}</p>
                    </CardHeader>
                    <CardContent className="flex-1 pt-4">
                      <div className="mb-6 pb-6 border-b border-stone-100">
                        <div className="flex items-baseline gap-2">
                          <span className="text-5xl font-bold text-stone-900 tracking-tight font-[family-name:var(--font-display)]">{opt.price}</span>
                          <span className="text-stone-500 text-lg">{opt.unit}</span>
                        </div>
                      </div>
                      <ul className="space-y-3.5">{opt.features.map((f, i) => <li key={i} className="flex items-start gap-3"><div className="mt-0.5 w-5 h-5 rounded-full bg-emerald-50 flex items-center justify-center shrink-0"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /></div><span className="text-sm text-stone-700 leading-relaxed">{f}</span></li>)}</ul>
                    </CardContent>
                    <CardFooter className="pt-4 pb-6"><a href="#kontakt" className="w-full"><Button className={`w-full rounded-full h-12 text-base font-medium transition-all active:scale-[0.97] ${opt.highlighted ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/25' : 'bg-stone-900 hover:bg-stone-800 text-white'}`}>Välj {opt.name} <ArrowRight className="w-4 h-4 ml-2" /></Button></a></CardFooter>
                  </Card>
                ))}
              </div>
            </div>

            <div className="bg-stone-50 rounded-2xl p-8 sm:p-12 max-w-4xl mx-auto">
              <h3 className="text-2xl font-bold text-stone-900 mb-6 text-center font-[family-name:var(--font-display)]">Hur det fungerar</h3>
              <div className="space-y-4 text-stone-600 leading-relaxed">
                <p>Du köper din hemsida via ett av två alternativ. Vid <strong className="text-stone-900">direktköp</strong> betalar du 35 000 kr och äger hemsidan fullt ut från dag ett — fri att hosta hos oss, hos någon annan eller på egen hand.</p>
                <p>Vid <strong className="text-stone-900">avbetalning 2 år</strong> betalar du 2 000 kr per månad i 24 månader. Under perioden ingår drift, support och en större omfaktorering. När perioden är slut övergår full äganderätt till dig.</p>
                <p><strong className="text-stone-900">Du äger alltid din domän och din kod.</strong> Vi bygger, du bestämmer — precis som varumärket lovar.</p>
              </div>
            </div>
          </div>
        </section>

        {/* PROCESS — Dark, compact */}
        <section id="process" className="py-24 sm:py-32 bg-stone-900 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16 reveal" ref={processRef}>
              <h2 className="text-3xl sm:text-5xl font-bold mb-4 font-[family-name:var(--font-display)]">Fyra enkla steg</h2>
              <p className="text-lg text-stone-400">Från samtal till lansering. Vi gör det enkelt.</p>
            </div>
            <div className="relative grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
              <div className="hidden lg:block absolute top-12 left-[12.5%] right-[12.5%] h-px bg-gradient-to-r from-transparent via-stone-700 to-transparent" />
              {[{ n: '01', icon: MessageCircle, t: 'Vi pratar', d: 'Du berättar om ditt företag och vad du behöver. Vi lyssnar och ger råd.' }, { n: '02', icon: Palette, t: 'Vi designar', d: 'Vi skapar en unik design som speglar ditt företags identitet. Du justerar tills du är nöjd.' }, { n: '03', icon: Server, t: 'Vi bygger', d: 'Vi bygger din hemsida, ordnar .SE-domän, e-post, SSL och hosting. Allt driftklart.' }, { n: '04', icon: Shield, t: 'Du äger', d: 'Vid direktköp äger du allt från dag 1. Vid avbetalning äger du allt när perioden är slut.' }].map(s => { const Icon = s.icon; return (
                <div key={s.n} className="relative text-center group">
                  <div className="relative inline-flex w-16 h-16 rounded-2xl bg-stone-800 ring-1 ring-stone-700 items-center justify-center mb-5 group-hover:bg-blue-600 group-hover:ring-blue-500 transition-all duration-300">
                    <Icon className="w-7 h-7 text-stone-400 group-hover:text-white transition-colors" />
                    <span className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-blue-600 text-white text-xs font-bold flex items-center justify-center ring-4 ring-stone-900 font-[family-name:var(--font-display)]">{s.n}</span>
                  </div>
                  <h3 className="text-xl font-bold mb-3 font-[family-name:var(--font-display)]">{s.t}</h3>
                  <p className="text-stone-400 leading-relaxed text-sm">{s.d}</p>
                </div>); })}
            </div>
          </div>
        </section>

        {/* STATS — Compact, punchy */}
        <section className="relative py-14 bg-stone-950 overflow-hidden">
          <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, white 1px, transparent 0)', backgroundSize: '32px 32px' }} />
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center text-white">
              {[['99.9%', 'Upptid'], ['< 2s', 'Laddtid'], ['24/7', 'Övervakning'], ['30 dag', 'Backup-historik']].map(([v, l]) => (
                <div key={l} className="space-y-1"><div className="text-4xl sm:text-5xl font-bold tracking-tight font-[family-name:var(--font-display)]">{v}</div><div className="text-stone-500 text-sm font-medium">{l}</div></div>
              ))}
            </div>
          </div>
        </section>

        {/* TESTIMONIALS — With larger quote marks and breathing room */}
        <section className="py-24 sm:py-32 bg-stone-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16 reveal" ref={testimonialsRef}>
              <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">Vad våra kunder säger</h2>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
              {testimonials.map(t => (
                <Card key={t.name} className="relative border-stone-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-white overflow-hidden">
                  <div className="absolute top-2 right-4 text-8xl leading-none text-stone-100 font-serif select-none pointer-events-none">&ldquo;</div>
                  <CardHeader className="pb-2 relative">
                    <div className="flex gap-0.5 mb-3">{Array.from({ length: t.stars }).map((_, i) => <Star key={i} className="w-4 h-4 fill-stone-800 text-stone-800" />)}</div>
                  </CardHeader>
                  <CardContent className="relative">
                    <p className="text-stone-700 leading-relaxed mb-6 text-[0.95rem]">&ldquo;{t.text}&rdquo;</p>
                    <div className="flex items-center gap-3 pt-4 border-t border-stone-100">
                      <div className="w-10 h-10 rounded-full bg-stone-900 text-white font-semibold text-sm flex items-center justify-center shrink-0 font-[family-name:var(--font-display)]">
                        {t.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
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

        {/* ABOUT — Asymmetric: text left, visual right */}
        <section id="om-oss" className="py-24 sm:py-32 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-5 gap-16 items-center reveal" ref={aboutRef}>
              <div className="lg:col-span-3">
                <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-8 font-[family-name:var(--font-display)]">Vi förstår svenska företag — och webben</h2>
                <div className="space-y-5 text-stone-500 leading-relaxed text-lg">
                  <p>Ownli grundades med en enkel idé: svenska företag förtjänar bättre hemsidor. För ofta ser vi fantastiska företag med dåliga, långsamma eller osäkra hemsidor som kostar för mycket.</p>
                  <p>Vi kombinerar djup teknisk expertis inom WordPress, hosting och webbsäkerhet med en genuin förståelse för olika branschers unika behov.</p>
                </div>
                <div className="mt-10 flex flex-wrap gap-8">
                  {[{ icon: Shield, t: 'Säker hosting', s: 'Imunify360 + WAF' }, { icon: Globe, t: '.SE-domäner', s: 'Certifierade registrarer' }, { icon: Headphones, t: 'Svensk support', s: 'Personlig & snabb' }].map(x => { const Icon = x.icon; return (
                    <div key={x.t} className="flex items-center gap-3"><div className="w-11 h-11 rounded-lg bg-stone-100 flex items-center justify-center"><Icon className="w-5 h-5 text-stone-700" /></div><div><p className="font-semibold text-stone-900 text-sm font-[family-name:var(--font-display)]">{x.t}</p><p className="text-xs text-stone-500">{x.s}</p></div></div>
                  ); })}
                </div>
              </div>
              <div className="lg:col-span-2 relative">
                <div className="aspect-[3/4] rounded-2xl bg-stone-100 flex items-center justify-center relative overflow-hidden border border-stone-200">
                  <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, #1c1917 1px, transparent 0)', backgroundSize: '24px 24px' }} />
                  <div className="text-center p-8 relative">
                    <div className="w-16 h-16 rounded-2xl bg-white shadow-lg flex items-center justify-center mx-auto mb-4">
                      <Server className="w-8 h-8 text-stone-700" />
                    </div>
                    <p className="text-stone-800 font-semibold text-lg font-[family-name:var(--font-display)]">Professionell infrastruktur</p>
                    <p className="text-stone-500 text-sm mt-1">WHM/cPanel · LiteSpeed · CloudLinux</p>
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

        {/* FAQ — With smooth animation */}
        <section className="py-24 sm:py-32 bg-stone-50">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16 reveal" ref={faqRef}>
              <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 font-[family-name:var(--font-display)]">Frågor och svar</h2>
            </div>
            <div className="space-y-3">
              {faqs.map((faq, i) => (
                <div key={i} className={`bg-white rounded-xl border overflow-hidden transition-all duration-200 ${faqOpen === i ? 'border-stone-400 shadow-md' : 'border-stone-200 hover:border-stone-300'}`}>
                  <button className="w-full px-6 py-5 text-left flex items-center justify-between gap-4 hover:bg-stone-50/50 transition-colors" onClick={() => setFaqOpen(faqOpen === i ? null : i)} aria-expanded={faqOpen === i}>
                    <span className="font-medium text-stone-900 font-[family-name:var(--font-display)]">{faq.q}</span>
                    <div className={`shrink-0 w-7 h-7 rounded-full flex items-center justify-center transition-all duration-200 ${faqOpen === i ? 'bg-stone-900 rotate-90' : 'bg-stone-100'}`}>
                      <ChevronRight className={`w-4 h-4 transition-colors duration-200 ${faqOpen === i ? 'text-white' : 'text-stone-500'}`} />
                    </div>
                  </button>
                  <div className={`faq-expand ${faqOpen === i ? 'open' : ''}`}>
                    <div>
                      <div className="px-6 pb-5 text-stone-600 leading-relaxed text-[0.95rem]">{faq.a}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CONTACT — Asymmetric: info left, form right */}
        <section id="kontakt" className="py-24 sm:py-32 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-5 gap-16 reveal" ref={contactRef}>
              <div className="lg:col-span-2">
                <h2 className="text-3xl sm:text-5xl font-bold text-stone-900 mb-6 font-[family-name:var(--font-display)]">Redo att synas online?</h2>
                <p className="text-lg text-stone-500 mb-10 leading-relaxed">Berätta om ditt företag och vilka behov du har. Vi återkommer med ett förslag inom 24 timmar — helt kostnadsfritt.</p>
                <div className="space-y-6">
                  {[{ icon: Mail, t: 'E-post', d: 'hej@ownli.se' }, { icon: Clock, t: 'Svarstid', d: 'Inom 24 timmar vardagar' }, { icon: Search, t: 'Gratis konsultation', d: 'Vi analyserar din nuvarande närvaro' }].map(x => { const Icon = x.icon; return (
                    <div key={x.t} className="flex items-start gap-4"><div className="w-12 h-12 rounded-xl bg-stone-100 flex items-center justify-center shrink-0"><Icon className="w-6 h-6 text-stone-700" /></div><div><p className="font-semibold text-stone-900 font-[family-name:var(--font-display)]">{x.t}</p><p className="text-stone-500">{x.d}</p></div></div>
                  ); })}
                </div>
              </div>
              <div className="lg:col-span-3">
                <Card className="border-stone-200 shadow-lg shadow-stone-200/40">
                  <CardHeader className="pb-2"><CardTitle className="text-xl text-stone-900 font-[family-name:var(--font-display)]">Skicka förfrågan</CardTitle><p className="text-sm text-stone-500">Vi återkommer inom 24 timmar — kostnadsfritt.</p></CardHeader>
                  <CardContent className="pt-4">
                    <form onSubmit={handleContact} className="space-y-4">
                      <div>
                        <label className="block text-xs font-semibold text-stone-700 mb-1.5 uppercase tracking-wide">Företagets namn</label>
                        <Input name="company" placeholder="T.ex. Acme AB" className="h-11 border-stone-300 focus:border-stone-900 focus:ring-2 focus:ring-stone-200 transition-all" required />
                      </div>
                      <div className="grid sm:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-xs font-semibold text-stone-700 mb-1.5 uppercase tracking-wide">Ditt namn</label>
                          <Input name="name" placeholder="För- och efternamn" className="h-11 border-stone-300 focus:border-stone-900 focus:ring-2 focus:ring-stone-200 transition-all" required />
                        </div>
                        <div>
                          <label className="block text-xs font-semibold text-stone-700 mb-1.5 uppercase tracking-wide">E-post</label>
                          <Input name="email" type="email" placeholder="namn@foretag.se" className="h-11 border-stone-300 focus:border-stone-900 focus:ring-2 focus:ring-stone-200 transition-all" required />
                        </div>
                      </div>
                      <div>
                        <label className="block text-xs font-semibold text-stone-700 mb-1.5 uppercase tracking-wide">Telefon</label>
                        <Input name="phone" type="tel" placeholder="070-123 45 67" className="h-11 border-stone-300 focus:border-stone-900 focus:ring-2 focus:ring-stone-200 transition-all" />
                      </div>
                      <div>
                        <label className="block text-xs font-semibold text-stone-700 mb-1.5 uppercase tracking-wide">Berätta om ditt företag</label>
                        <Textarea name="message" placeholder="Vilken bransch är ni i? Vad behöver ni för funktioner? Har ni redan en domän?" className="border-stone-300 focus:border-stone-900 focus:ring-2 focus:ring-stone-200 transition-all min-h-[120px]" />
                      </div>
                      <Button type="submit" className="w-full bg-stone-900 hover:bg-stone-800 text-white rounded-full h-12 text-base shadow-lg active:scale-[0.97] transition-transform">{contactSent ? <span className="flex items-center gap-2"><CheckCircle2 className="w-5 h-5" />{'Tack! Vi hör av oss snart.'}</span> : <>{'Skicka förfrågan'} <ArrowRight className="w-4 h-4 ml-2" /></>}</Button>
                    </form>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* FOOTER — Fixed contrast: stone-300 instead of stone-400/500 */}
      <footer className="bg-stone-900 text-stone-300 pt-16 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
            <div className="sm:col-span-2 lg:col-span-1">
              <div className="flex items-center gap-2.5 mb-4"><OwnliLogo size={36} markOnly /><span className="text-xl font-bold text-white font-[family-name:var(--font-display)]">Ownli</span></div>
              <p className="text-sm leading-relaxed mb-5 text-stone-400">Professionella hemsidor för svenska företag. Design, hosting, domän och e-post — allt i ett.</p>
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-stone-800 text-xs">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-stone-300">Alla system opererar normalt</span>
              </div>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4 text-sm font-[family-name:var(--font-display)]">Tjänster</h4>
              <ul className="space-y-2.5 text-sm">
                {['Webbdesign', 'WordPress', '.SE-domän', 'E-post', 'Hosting'].map(s => <li key={s} className="hover:text-white transition-colors cursor-pointer">{s}</li>)}
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4 text-sm font-[family-name:var(--font-display)]">Support</h4>
              <ul className="space-y-2.5 text-sm">
                {['Kontakta oss', 'Vanliga frågor', 'cPanel-guide', 'Statussida'].map(s => <li key={s} className="hover:text-white transition-colors cursor-pointer">{s}</li>)}
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4 text-sm font-[family-name:var(--font-display)]">Legal</h4>
              <ul className="space-y-2.5 text-sm">
                {['Villkor', 'Integritetspolicy', 'Cookies'].map(s => <li key={s} className="hover:text-white transition-colors cursor-pointer">{s}</li>)}
              </ul>
            </div>
          </div>
          <div className="border-t border-stone-800 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm">
            <p className="text-stone-400">&copy; {new Date().getFullYear()} Ownli. Alla rättigheter förbehållna.</p>
            <p className="text-stone-500 text-xs">Du äger. Vi bygger. <span className="text-stone-700">·</span> Byggt i Sverige</p>
          </div>
        </div>
      </footer>

      {/* MOBILE STICKY CTA */}
      <div className="fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-t border-stone-200 p-3 lg:hidden safe-area-bottom">
        <a href="#kontakt"><Button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-full h-12 text-base shadow-lg active:scale-[0.97] transition-transform">Kom igång <ArrowRight className="w-4 h-4 ml-2" /></Button></a>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   MAIN PAGE
   ═══════════════════════════════════════════ */
export default function Home() {
  return <LandingPage />;
}
