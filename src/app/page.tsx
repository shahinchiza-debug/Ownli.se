'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  Globe, Mail, Shield, Smartphone, Clock, CheckCircle2, ArrowRight,
  Menu, X, ChevronRight, Star, UtensilsCrossed, Server, Palette, Search,
  MessageCircle, BarChart3, Headphones, Hammer, Heart, Scale, ShoppingCart,
  GraduationCap, Building, Sparkles, Home, Users, FileText, Inbox, Settings,
  LogOut, Plus, Trash2, Eye, EyeOff, ChevronDown, TrendingUp, DollarSign,
  AlertCircle, CheckCircle, XCircle, Edit, LayoutDashboard, FolderOpen,
  Receipt, MessageSquare,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import ShaderHero from '@/components/ShaderHero';
import OwnliLogo from '@/components/OwnliLogo';

/* ─── Types ─── */
type View = 'landing' | 'login' | 'dashboard';
type DashSection = 'overview' | 'customers' | 'projects' | 'invoices' | 'messages' | 'settings';
interface Customer { id: string; companyName: string; contactName: string; email: string; phone?: string; industry?: string; plan: string; status: string; notes?: string; createdAt: string; }
interface Project { id: string; customerId: string; name: string; description?: string; status: string; startDate: string; customer?: { companyName: string }; }
interface Invoice { id: string; customerId: string; amount: number; description: string; status: string; dueDate: string; customer?: { companyName: string }; }
interface ContactMsg { id: string; name: string; email: string; phone?: string; company?: string; message: string; read: boolean; createdAt: string; }
interface Stats { totalCustomers: number; activeProjects: number; revenueThisMonth: number; unpaidInvoices: number; unreadMessages: number; recentCustomers: Customer[]; recentMessages: ContactMsg[]; }

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

/* Hero-varianter: [före, markera, efter] + underrubrik. Plockas slumpmässigt vid varje sidladdning. */
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

const statusColors: Record<string, string> = { active: 'bg-emerald-100 text-emerald-700', paused: 'bg-amber-100 text-amber-700', cancelled: 'bg-red-100 text-red-700', planning: 'bg-blue-100 text-blue-700', in_progress: 'bg-amber-100 text-amber-700', review: 'bg-purple-100 text-purple-700', completed: 'bg-emerald-100 text-emerald-700', pending: 'bg-amber-100 text-amber-700', paid: 'bg-emerald-100 text-emerald-700', overdue: 'bg-red-100 text-red-700' };
const statusLabels: Record<string, string> = { active: 'Aktiv', paused: 'Pausad', cancelled: 'Avslutad', planning: 'Planering', in_progress: 'Pågående', review: 'Granskning', completed: 'Klar', pending: 'Väntar', paid: 'Betald', overdue: 'Försenad' };

/* ═══════════════════════════════════════════
   LANDING PAGE
   ═══════════════════════════════════════════ */
function LandingPage({ onLogin }: { onLogin: () => void }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [faqOpen, setFaqOpen] = useState<number | null>(null);
  const [contactSent, setContactSent] = useState(false);
  // Slumpa hero-variant vid varje sidladdning (refresh).
  const [heroIdx] = useState(() => Math.floor(Math.random() * heroVariants.length));
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

  return (
    <div className="min-h-screen flex flex-col">
      {/* NAVBAR */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-md shadow-sm border-b border-stone-200' : 'bg-transparent'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 sm:h-20">
            <a href="#" className="flex items-center gap-2.5 group">
              <OwnliLogo size={36} markOnly />
              <span className="text-xl font-bold text-stone-900 group-hover:text-blue-700 transition-colors">Ownli</span>
            </a>
            <div className="hidden md:flex items-center gap-6">
              {navLinks.map(l => <a key={l.href} href={l.href} className="text-sm font-medium text-stone-600 hover:text-blue-700 transition-colors">{l.label}</a>)}
              <Button variant="outline" size="sm" className="border-stone-300 text-stone-700 hover:bg-stone-50 rounded-full" onClick={onLogin}>Logga in</Button>
              <a href="#kontakt"><Button className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-6">Kom igång</Button></a>
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
              <Button variant="outline" className="w-full border-stone-300 rounded-full" onClick={() => { setMobileOpen(false); onLogin(); }}>Logga in</Button>
              <a href="#kontakt" onClick={() => setMobileOpen(false)}><Button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-full mt-2">Kom igång</Button></a>
            </div>
          </div>
        )}
      </nav>

      <main className="flex-1">
        {/* HERO */}
        <section className="relative min-h-screen flex items-center overflow-hidden">
          <ShaderHero className="bg-stone-950" />
          {/* Subtle dark overlay så texten blir lättare att läsa */}
          <div className="absolute inset-0 bg-gradient-to-br from-stone-950/40 via-stone-900/20 to-stone-950/60 pointer-events-none" />
          <div className="absolute inset-0 bg-gradient-to-t from-stone-950/70 via-transparent to-transparent pointer-events-none" />
          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 sm:py-40 w-full">
            <div className="max-w-3xl mx-auto text-center">
              <div className="mb-6 inline-flex items-center gap-2 text-blue-300 text-sm font-semibold tracking-[0.2em] uppercase"><span className="h-px w-8 bg-blue-400/60" />Du äger. Vi bygger.<span className="h-px w-8 bg-blue-400/60" /></div>
              <h1 className="text-4xl sm:text-5xl lg:text-7xl font-bold text-white leading-tight mb-6" suppressHydrationWarning>{hero.title[0]}<span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-blue-300">{hero.title[1]}</span>{hero.title[2]}</h1>
              <p className="text-lg sm:text-xl text-stone-200 mb-10 max-w-2xl mx-auto leading-relaxed" suppressHydrationWarning>{hero.subtitle}</p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="#priser"><Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-8 text-lg h-14 w-full sm:w-auto shadow-lg shadow-blue-600/25">Se våra priser <ArrowRight className="w-5 h-5 ml-2" /></Button></a>
                <a href="#process"><Button size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10 rounded-full px-8 text-lg h-14 w-full sm:w-auto">Så fungerar det</Button></a>
              </div>
              <div className="mt-10 flex flex-wrap justify-center gap-x-8 gap-y-3 text-stone-300">
                {[['.SE-domän ingår', true], ['SSL/HTTPS inkluderat', true], ['Svensk support', true], ['99.9% upptid', true]].map(([l, ok]) => (
                  <div key={l as string} className="flex items-center gap-2"><CheckCircle2 className="w-5 h-5 text-emerald-400" /><span className="text-sm">{l}</span></div>
                ))}
              </div>
            </div>
          </div>
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce"><div className="w-6 h-10 rounded-full border-2 border-white/30 flex items-start justify-center pt-2"><div className="w-1.5 h-3 rounded-full bg-white/50" /></div></div>
        </section>

        {/* SERVICES */}
        <section id="tjanster" className="py-20 sm:py-28 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-4">Allt ditt företag behöver på nätet</h2>
              <p className="text-lg text-stone-600">Från domän och hosting till design och e-post — vi hanterar allt tekniskt så att du kan fokusera på din verksamhet.</p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
              {services.map(s => { const Icon = s.icon; return (
                <Card key={s.title} className="group border-stone-200 hover:border-blue-300 hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                  <CardHeader><div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center mb-3 group-hover:bg-blue-600 transition-colors"><Icon className="w-6 h-6 text-blue-700 group-hover:text-white transition-colors" /></div><CardTitle className="text-xl text-stone-900">{s.title}</CardTitle></CardHeader>
                  <CardContent><p className="text-stone-600 leading-relaxed">{s.desc}</p></CardContent>
                </Card>); })}
            </div>
          </div>
        </section>

        {/* INDUSTRIES */}
        <section id="branscher" className="py-20 sm:py-28 bg-stone-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-4">Vi servar alla branscher</h2>
              <p className="text-lg text-stone-600">Oavsett bransch hjälper vi ditt företag att synas online</p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {industries.map(ind => { const Icon = ind.icon; return (
                <Card key={ind.name} className="group border-stone-200 hover:border-blue-300 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 text-center">
                  <CardHeader className="items-center pb-2"><div className="w-14 h-14 rounded-2xl bg-blue-100 flex items-center justify-center mb-2 group-hover:bg-blue-600 transition-colors"><Icon className="w-7 h-7 text-blue-700 group-hover:text-white transition-colors" /></div><CardTitle className="text-lg text-stone-900">{ind.name}</CardTitle></CardHeader>
                  <CardContent><p className="text-stone-600 text-sm">{ind.desc}</p></CardContent>
                </Card>); })}
            </div>
          </div>
        </section>

        {/* PRICING */}
        <section id="priser" className="py-20 sm:py-28 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-4">Transparenta priser — du äger, vi bygger</h2>
              <p className="text-lg text-stone-600">Två enkla sätt att bli ägare. Alla priser är exkl. moms.</p>
            </div>

            {/* Köpalternativ */}
            <div className="mb-16">
              <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                {purchaseOptions.map(opt => (
                  <Card key={opt.name} className={`relative flex flex-col transition-all duration-300 hover:-translate-y-1 ${opt.highlighted ? 'border-2 border-blue-500 shadow-xl shadow-blue-500/10 scale-[1.02]' : 'border-stone-200 hover:shadow-lg'}`}>
                    {opt.highlighted && <div className="absolute -top-4 left-1/2 -translate-x-1/2"><Badge className="bg-blue-600 text-white px-4 py-1 text-sm">Mest populär</Badge></div>}
                    <CardHeader className="pb-2"><CardTitle className="text-2xl text-stone-900">{opt.name}</CardTitle><p className="text-stone-500 text-sm">{opt.desc}</p></CardHeader>
                    <CardContent className="flex-1">
                      <div className="mb-6">
                        <span className="text-4xl font-bold text-stone-900">{opt.price}</span>
                        <span className="text-stone-500 text-lg"> {opt.unit}</span>
                      </div>
                      <ul className="space-y-3">{opt.features.map((f, i) => <li key={i} className="flex items-start gap-2.5"><CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" /><span className="text-sm text-stone-700">{f}</span></li>)}</ul>
                    </CardContent>
                    <CardFooter><a href="#kontakt" className="w-full"><Button className={`w-full rounded-full h-12 text-base font-medium ${opt.highlighted ? 'bg-blue-600 hover:bg-blue-700 text-white' : 'bg-stone-900 hover:bg-stone-800 text-white'}`}>Välj {opt.name} <ArrowRight className="w-4 h-4 ml-2" /></Button></a></CardFooter>
                  </Card>
                ))}
              </div>
            </div>

            {/* Hur det fungerar */}
            <div className="bg-stone-50 rounded-2xl p-8 sm:p-12 max-w-4xl mx-auto">
              <h3 className="text-2xl font-bold text-stone-900 mb-6 text-center">Hur det fungerar</h3>
              <div className="space-y-4 text-stone-600 leading-relaxed">
                <p>Du köper din hemsida via ett av två alternativ. Vid <strong className="text-stone-900">direktköp</strong> betalar du 35 000 kr och äger hemsidan fullt ut från dag ett — fri att hosta hos oss, hos någon annan eller på egen hand.</p>
                <p>Vid <strong className="text-stone-900">avbetalning 2 år</strong> betalar du 2 000 kr per månad i 24 månader. Under perioden ingår drift, support och en större omfaktorering. När perioden är slut övergår full äganderätt till dig.</p>
                <p><strong className="text-stone-900">Du äger alltid din domän och din kod.</strong> Vi bygger, du bestämmer — precis som varumärket lovar: "Du äger. Vi bygger."</p>
              </div>
            </div>
          </div>
        </section>

        {/* PROCESS */}
        <section id="process" className="py-20 sm:py-28 bg-stone-900 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold mb-4">Från samtal till lansering — fyra enkla steg</h2>
              <p className="text-lg text-stone-400">Vi gör det enkelt. Du äger resultatet, vi bygger vägen dit.</p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
              {[{ n: '01', icon: MessageCircle, t: 'Vi pratar', d: 'Du berättar om ditt företag och vad du behöver. Vi lyssnar och ger råd om vilka funktioner som passar bäst.' }, { n: '02', icon: Palette, t: 'Vi designar', d: 'Vi skapar en unik design som speglar ditt företags identitet. Du får justera tills du är nöjd.' }, { n: '03', icon: Server, t: 'Vi bygger', d: 'Vi bygger din hemsida, ordnar .SE-domän, e-post, SSL och hosting. Allt driftklart.' }, { n: '04', icon: Shield, t: 'Du äger', d: 'Vid direktköp äger du allt från dag 1. Vid avbetalning äger du allt när perioden är slut. Du är alltid ägare av din kod och din domän.' }].map(s => { const Icon = s.icon; return (
                <div key={s.n} className="relative text-center group">
                  <div className="text-6xl font-black text-blue-600/20 mb-2 group-hover:text-blue-600/30 transition-colors">{s.n}</div>
                  <div className="w-14 h-14 rounded-2xl bg-blue-600/20 flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-600/30 transition-colors"><Icon className="w-7 h-7 text-blue-400" /></div>
                  <h3 className="text-xl font-bold mb-3">{s.t}</h3>
                  <p className="text-stone-400 leading-relaxed">{s.d}</p>
                </div>); })}
            </div>
          </div>
        </section>

        {/* STATS */}
        <section className="py-12 bg-blue-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center text-white">
              {[['99.9%', 'Upptid'], ['< 2s', 'Laddtid'], ['24/7', 'Övervakning'], ['30 dag', 'Backup-historik']].map(([v, l]) => (
                <div key={l}><div className="text-3xl sm:text-4xl font-bold">{v}</div><div className="text-blue-200 text-sm mt-1">{l}</div></div>
              ))}
            </div>
          </div>
        </section>

        {/* TESTIMONIALS */}
        <section className="py-20 sm:py-28 bg-stone-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-4">Vad våra kunder säger</h2>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
              {testimonials.map(t => (
                <Card key={t.name} className="border-stone-200 hover:shadow-lg transition-shadow duration-300">
                  <CardHeader><div className="flex gap-0.5 mb-2">{Array.from({ length: t.stars }).map((_, i) => <Star key={i} className="w-5 h-5 fill-blue-400 text-blue-400" />)}</div></CardHeader>
                  <CardContent><p className="text-stone-700 leading-relaxed italic mb-4">&ldquo;{t.text}&rdquo;</p><div><p className="font-semibold text-stone-900">{t.name}</p><p className="text-sm text-stone-500">{t.role}</p></div></CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* ABOUT */}
        <section id="om-oss" className="py-20 sm:py-28 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              <div>
                <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-6">Vi förstår svenska företag — och webben</h2>
                <div className="space-y-4 text-stone-600 leading-relaxed">
                  <p>Ownli grundades med en enkel idé: svenska företag förtjänar bättre hemsidor. För ofta ser vi fantastiska företag med dåliga, långsamma eller osäkra hemsidor som kostar för mycket.</p>
                  <p>Vi kombinerar djup teknisk expertis inom WordPress, hosting och webbsäkerhet med en genuin förståelse för olika branschers unika behov.</p>
                  <p>Vår infrastruktur bygger på WHM/cPanel hosting med CloudLinux, LiteSpeed och Imunify360 — samma teknik som stora webbhotell använder, men med personlig service.</p>
                </div>
                <div className="mt-8 flex flex-wrap gap-6">
                  {[{ icon: Shield, t: 'Säker hosting', s: 'Imunify360 + WAF' }, { icon: Globe, t: '.SE-domäner', s: 'Certifierade registrarer' }, { icon: Headphones, t: 'Svensk support', s: 'Personlig & snabb' }].map(x => { const Icon = x.icon; return (
                    <div key={x.t} className="flex items-center gap-2"><div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center"><Icon className="w-5 h-5 text-blue-700" /></div><div><p className="font-semibold text-stone-900 text-sm">{x.t}</p><p className="text-xs text-stone-500">{x.s}</p></div></div>
                  ); })}
                </div>
              </div>
              <div className="relative">
                <div className="aspect-[4/3] rounded-2xl bg-gradient-to-br from-blue-200 via-blue-100 to-stone-200 flex items-center justify-center"><div className="text-center p-8"><Server className="w-20 h-20 text-blue-600 mx-auto mb-4" /><p className="text-blue-800 font-semibold text-lg">Professionell infrastruktur</p><p className="text-blue-700 text-sm mt-1">WHM/cPanel · LiteSpeed · CloudLinux</p></div></div>
                <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-blue-600 rounded-2xl flex items-center justify-center text-white shadow-lg"><div className="text-center"><div className="text-3xl font-bold">5+</div><div className="text-xs text-blue-200">Års erfarenhet</div></div></div>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="py-20 sm:py-28 bg-stone-50">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl sm:text-4xl font-bold text-stone-900">Frågor och svar</h2>
            </div>
            <div className="space-y-3">
              {faqs.map((faq, i) => (
                <div key={i} className="bg-white rounded-xl border border-stone-200 overflow-hidden">
                  <button className="w-full px-6 py-5 text-left flex items-center justify-between gap-4 hover:bg-stone-50 transition-colors" onClick={() => setFaqOpen(faqOpen === i ? null : i)}>
                    <span className="font-medium text-stone-900">{faq.q}</span>
                    <ChevronRight className={`w-5 h-5 text-stone-400 shrink-0 transition-transform duration-200 ${faqOpen === i ? 'rotate-90' : ''}`} />
                  </button>
                  {faqOpen === i && <div className="px-6 pb-5 text-stone-600 leading-relaxed">{faq.a}</div>}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CONTACT */}
        <section id="kontakt" className="py-20 sm:py-28 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-16">
              <div>
                <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-6">Redo att synas online?</h2>
                <p className="text-lg text-stone-600 mb-10 leading-relaxed">Berätta om ditt företag och vilka behov du har. Vi återkommer med ett förslag inom 24 timmar — helt kostnadsfritt.</p>
                <div className="space-y-6">
                  {[{ icon: Mail, t: 'E-post', d: 'hej@ownli.se' }, { icon: Clock, t: 'Svarstid', d: 'Inom 24 timmar vardagar' }, { icon: Search, t: 'Gratis konsultation', d: 'Vi analyserar din nuvarande närvaro' }].map(x => { const Icon = x.icon; return (
                    <div key={x.t} className="flex items-start gap-4"><div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center shrink-0"><Icon className="w-6 h-6 text-blue-700" /></div><div><p className="font-semibold text-stone-900">{x.t}</p><p className="text-stone-600">{x.d}</p></div></div>
                  ); })}
                </div>
              </div>
              <Card className="border-stone-200">
                <CardHeader><CardTitle className="text-xl text-stone-900">Skicka förfrågan</CardTitle></CardHeader>
                <CardContent>
                  <form onSubmit={handleContact} className="space-y-5">
                    <div><label className="block text-sm font-medium text-stone-700 mb-1.5">Företagets namn</label><Input name="company" placeholder="T.ex. Acme AB" className="h-11 border-stone-300" required /></div>
                    <div className="grid sm:grid-cols-2 gap-5">
                      <div><label className="block text-sm font-medium text-stone-700 mb-1.5">Ditt namn</label><Input name="name" placeholder="För- och efternamn" className="h-11 border-stone-300" required /></div>
                      <div><label className="block text-sm font-medium text-stone-700 mb-1.5">E-post</label><Input name="email" type="email" placeholder="namn@foretag.se" className="h-11 border-stone-300" required /></div>
                    </div>
                    <div><label className="block text-sm font-medium text-stone-700 mb-1.5">Telefon</label><Input name="phone" type="tel" placeholder="070-123 45 67" className="h-11 border-stone-300" /></div>
                    <div><label className="block text-sm font-medium text-stone-700 mb-1.5">Berätta om ditt företag</label><Textarea name="message" placeholder="Vilken bransch är ni i? Vad behöver ni för funktioner? Har ni redan en domän?" className="border-stone-300 min-h-[120px]" /></div>
                    <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-full h-12 text-base">{contactSent ? 'Tack! Vi hör av oss snart.' : 'Skicka förfrågan'}{!contactSent && <ArrowRight className="w-4 h-4 ml-2" />}</Button>
                  </form>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="bg-stone-900 text-stone-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-10">
            <div className="sm:col-span-2 lg:col-span-1">
              <div className="flex items-center gap-2.5 mb-4"><OwnliLogo size={36} markOnly /><span className="text-xl font-bold text-white">Ownli</span></div>
              <p className="text-sm leading-relaxed">Professionella hemsidor för svenska företag. Design, hosting, domän och e-post — allt i ett.</p>
            </div>
            <div><h4 className="text-white font-semibold mb-3">Tjänster</h4><ul className="space-y-2 text-sm"><li>Webbdesign</li><li>WordPress</li><li>.SE-domän</li><li>E-post</li><li>Hosting</li></ul></div>
            <div><h4 className="text-white font-semibold mb-3">Support</h4><ul className="space-y-2 text-sm"><li>Kontakta oss</li><li>Vanliga frågor</li><li>cPanel-guide</li><li>Statussida</li></ul></div>
            <div><h4 className="text-white font-semibold mb-3">Legal</h4><ul className="space-y-2 text-sm"><li>Villkor</li><li>Integritetspolicy</li><li>Cookies</li></ul></div>
          </div>
          <div className="border-t border-stone-800 pt-8 text-sm text-center">&copy; {new Date().getFullYear()} Ownli. Alla rättigheter förbehållna.</div>
        </div>
      </footer>
    </div>
  );
}

/* ═══════════════════════════════════════════
   LOGIN PAGE
   ═══════════════════════════════════════════ */
function LoginPage({ onLogin, onBack }: { onLogin: () => void; onBack: () => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPw, setShowPw] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
      const data = await res.json();
      if (res.ok) { onLogin(); }
      else { setError(data.error || 'Inloggningsfel'); }
    } catch { setError('Kunde inte ansluta till servern'); }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-stone-900 via-stone-800 to-blue-900 px-4">
      <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 50% 50%, rgba(59,130,246,0.4) 0%, transparent 60%)' }} />
      <Card className="w-full max-w-md relative z-10 shadow-2xl border-stone-200">
        <CardHeader className="text-center space-y-4 pb-2">
          <div className="flex items-center justify-center gap-2.5"><OwnliLogo size={40} markOnly /><span className="text-2xl font-bold text-stone-900">Ownli</span></div>
          <p className="text-stone-500">Logga in på din admin-panel</p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            {error && <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 flex items-center gap-2"><AlertCircle className="w-4 h-4 shrink-0" />{error}</div>}
            <div><label className="block text-sm font-medium text-stone-700 mb-1.5">E-post</label><Input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="admin@ownli.se" className="h-11" required /></div>
            <div><label className="block text-sm font-medium text-stone-700 mb-1.5">Lösenord</label>
              <div className="relative"><Input type={showPw ? 'text' : 'password'} value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" className="h-11 pr-10" required /><button type="button" className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400 hover:text-stone-600" onClick={() => setShowPw(!showPw)}>{showPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}</button></div>
            </div>
            <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white h-11 rounded-lg" disabled={loading}>{loading ? 'Loggar in...' : 'Logga in'}</Button>
          </form>
          <div className="mt-4 text-center text-xs text-stone-400">Standard: admin@ownli.se / admin123</div>
          <button onClick={onBack} className="mt-6 w-full text-center text-sm text-stone-500 hover:text-blue-700 transition-colors">&larr; Tillbaka till hemsidan</button>
        </CardContent>
      </Card>
    </div>
  );
}

/* ═══════════════════════════════════════════
   DASHBOARD
   ═══════════════════════════════════════════ */
function Dashboard({ onLogout }: { onLogout: () => void }) {
  const [section, setSection] = useState<DashSection>('overview');
  const [stats, setStats] = useState<Stats | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [messages, setMessages] = useState<ContactMsg[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      const [s, c, p, i, m] = await Promise.all([
        fetch('/api/stats').then(r => r.json()),
        fetch('/api/customers').then(r => r.json()),
        fetch('/api/projects').then(r => r.json()),
        fetch('/api/invoices').then(r => r.json()),
        fetch('/api/contact').then(r => r.json()),
      ]);
      setStats(s); setCustomers(c); setProjects(p); setInvoices(i); setMessages(m);
    } catch (e) { console.error('Fetch error', e); }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const navItems: { id: DashSection; label: string; icon: typeof Home }[] = [
    { id: 'overview', label: 'Översikt', icon: LayoutDashboard },
    { id: 'customers', label: 'Kunder', icon: Users },
    { id: 'projects', label: 'Projekt', icon: FolderOpen },
    { id: 'invoices', label: 'Fakturor', icon: Receipt },
    { id: 'messages', label: 'Meddelanden', icon: MessageSquare },
    { id: 'settings', label: 'Inställningar', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-stone-100 flex">
      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 z-40 w-64 bg-stone-900 text-white transform transition-transform duration-200 lg:translate-x-0 lg:static ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex items-center gap-2.5 px-6 h-16 border-b border-stone-800">
          <OwnliLogo size={32} markOnly />
          <span className="text-lg font-bold">Ownli</span>
        </div>
        <nav className="p-4 space-y-1">
          {navItems.map(n => { const Icon = n.icon; return (
            <button key={n.id} onClick={() => { setSection(n.id); setSidebarOpen(false); }} className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${section === n.id ? 'bg-blue-600 text-white' : 'text-stone-400 hover:text-white hover:bg-stone-800'}`}>
              <Icon className="w-5 h-5" />{n.label}
              {n.id === 'messages' && stats && stats.unreadMessages > 0 && <Badge className="ml-auto bg-red-500 text-white text-xs px-1.5 py-0">{stats.unreadMessages}</Badge>}
            </button>
          ); })}
        </nav>
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-stone-800">
          <button onClick={onLogout} className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-stone-400 hover:text-white hover:bg-stone-800 transition-colors"><LogOut className="w-5 h-5" />Logga ut</button>
        </div>
      </aside>

      {/* Overlay */}
      {sidebarOpen && <div className="fixed inset-0 z-30 bg-black/50 lg:hidden" onClick={() => setSidebarOpen(false)} />}

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="bg-white border-b border-stone-200 h-16 flex items-center px-4 sm:px-6 gap-4 shrink-0">
          <button className="lg:hidden p-2 -ml-2 text-stone-700" onClick={() => setSidebarOpen(true)}><Menu className="w-5 h-5" /></button>
          <h1 className="text-lg font-semibold text-stone-900 capitalize">{navItems.find(n => n.id === section)?.label || 'Översikt'}</h1>
        </header>

        <main className="flex-1 p-4 sm:p-6 overflow-auto">
          {!stats ? <div className="text-center py-20 text-stone-500">Laddar...</div> : (
            <>
              {section === 'overview' && <OverviewSection stats={stats} customers={customers} messages={messages} />}
              {section === 'customers' && <CustomersSection customers={customers} onRefresh={fetchData} />}
              {section === 'projects' && <ProjectsSection projects={projects} customers={customers} onRefresh={fetchData} />}
              {section === 'invoices' && <InvoicesSection invoices={invoices} customers={customers} onRefresh={fetchData} />}
              {section === 'messages' && <MessagesSection messages={messages} onRefresh={fetchData} />}
              {section === 'settings' && <SettingsSection />}
            </>
          )}
        </main>
      </div>
    </div>
  );
}

/* ─── Overview ─── */
function OverviewSection({ stats, customers, messages }: { stats: Stats; customers: Customer[]; messages: ContactMsg[] }) {
  const cards = [
    { label: 'Totalt kunder', value: stats.totalCustomers, icon: Users, color: 'bg-blue-100 text-blue-700' },
    { label: 'Aktiva projekt', value: stats.activeProjects, icon: FolderOpen, color: 'bg-blue-100 text-blue-700' },
    { label: 'Fakturerat i mån', value: `${stats.revenueThisMonth.toLocaleString('sv-SE')} kr`, icon: DollarSign, color: 'bg-emerald-100 text-emerald-700' },
    { label: 'Obetalda fakturor', value: stats.unpaidInvoices, icon: AlertCircle, color: 'bg-red-100 text-red-700' },
  ];
  return (
    <div className="space-y-6">
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map(c => { const Icon = c.icon; return (
          <Card key={c.label} className="border-stone-200"><CardContent className="p-5 flex items-center gap-4"><div className={`w-12 h-12 rounded-xl flex items-center justify-center ${c.color}`}><Icon className="w-6 h-6" /></div><div><p className="text-sm text-stone-500">{c.label}</p><p className="text-2xl font-bold text-stone-900">{c.value}</p></div></CardContent></Card>
        ); })}
      </div>
      <div className="grid lg:grid-cols-2 gap-6">
        <Card className="border-stone-200"><CardHeader><CardTitle className="text-lg">Senaste kunder</CardTitle></CardHeader><CardContent>
          <div className="space-y-3">{stats.recentCustomers.map(c => (
            <div key={c.id} className="flex items-center justify-between py-2 border-b border-stone-100 last:border-0">
              <div><p className="font-medium text-stone-900 text-sm">{c.companyName}</p><p className="text-xs text-stone-500">{c.industry} · {c.plan}</p></div>
              <Badge className={`${statusColors[c.status] || ''} text-xs`}>{statusLabels[c.status] || c.status}</Badge>
            </div>
          ))}</div>
        </CardContent></Card>
        <Card className="border-stone-200"><CardHeader><CardTitle className="text-lg">Senaste meddelanden</CardTitle></CardHeader><CardContent>
          <div className="space-y-3">{stats.recentMessages.map(m => (
            <div key={m.id} className="flex items-start gap-3 py-2 border-b border-stone-100 last:border-0">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${m.read ? 'bg-stone-100' : 'bg-blue-100'}`}><MessageSquare className={`w-4 h-4 ${m.read ? 'text-stone-400' : 'text-blue-600'}`} /></div>
              <div className="min-w-0"><p className={`text-sm ${m.read ? 'text-stone-600' : 'font-semibold text-stone-900'}`}>{m.name} — {m.company || m.email}</p><p className="text-xs text-stone-500 truncate">{m.message}</p></div>
            </div>
          ))}</div>
        </CardContent></Card>
      </div>
    </div>
  );
}

/* ─── Customers ─── */
function CustomersSection({ customers, onRefresh }: { customers: Customer[]; onRefresh: () => void }) {
  const [search, setSearch] = useState('');
  const [showAdd, setShowAdd] = useState(false);
  const [editId, setEditId] = useState<string | null>(null);
  const [form, setForm] = useState({ companyName: '', contactName: '', email: '', phone: '', industry: '', plan: 'Bas', status: 'active', notes: '' });

  const filtered = customers.filter(c => c.companyName.toLowerCase().includes(search.toLowerCase()) || c.contactName.toLowerCase().includes(search.toLowerCase()));

  const openAdd = () => { setForm({ companyName: '', contactName: '', email: '', phone: '', industry: '', plan: 'Bas', status: 'active', notes: '' }); setShowAdd(true); };
  const openEdit = (c: Customer) => { setForm({ companyName: c.companyName, contactName: c.contactName, email: c.email, phone: c.phone || '', industry: c.industry || '', plan: c.plan, status: c.status, notes: c.notes || '' }); setEditId(c.id); };

  const saveCustomer = async () => {
    if (editId) { await fetch(`/api/customers/${editId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) }); }
    else { await fetch('/api/customers', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) }); }
    setShowAdd(false); setEditId(null); onRefresh();
  };

  const deleteCustomer = async (id: string) => { if (confirm('Ta bort denna kund?')) { await fetch(`/api/customers/${id}`, { method: 'DELETE' }); onRefresh(); } };

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row gap-3 sm:items-center justify-between">
        <div className="relative flex-1 max-w-sm"><Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-stone-400" /><Input placeholder="Sök kund..." value={search} onChange={e => setSearch(e.target.value)} className="pl-9 h-10" /></div>
        <Button onClick={openAdd} className="bg-blue-600 hover:bg-blue-700 text-white"><Plus className="w-4 h-4 mr-2" />Ny kund</Button>
      </div>

      <Card className="border-stone-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead><tr className="bg-stone-50 border-b border-stone-200"><th className="text-left px-4 py-3 font-medium text-stone-500">Företag</th><th className="text-left px-4 py-3 font-medium text-stone-500">Kontakt</th><th className="text-left px-4 py-3 font-medium text-stone-500 hidden md:table-cell">Bransch</th><th className="text-left px-4 py-3 font-medium text-stone-500">Paket</th><th className="text-left px-4 py-3 font-medium text-stone-500">Status</th><th className="text-right px-4 py-3 font-medium text-stone-500">Åtgärd</th></tr></thead>
            <tbody>{filtered.map(c => (
              <tr key={c.id} className="border-b border-stone-100 hover:bg-stone-50"><td className="px-4 py-3 font-medium text-stone-900">{c.companyName}</td><td className="px-4 py-3 text-stone-600">{c.contactName}</td><td className="px-4 py-3 text-stone-600 hidden md:table-cell">{c.industry}</td><td className="px-4 py-3"><Badge variant="secondary" className="text-xs">{c.plan}</Badge></td><td className="px-4 py-3"><Badge className={`${statusColors[c.status] || ''} text-xs`}>{statusLabels[c.status] || c.status}</Badge></td><td className="px-4 py-3 text-right"><button onClick={() => openEdit(c)} className="p-1 text-stone-400 hover:text-blue-600"><Edit className="w-4 h-4" /></button><button onClick={() => deleteCustomer(c.id)} className="p-1 text-stone-400 hover:text-red-600 ml-1"><Trash2 className="w-4 h-4" /></button></td></tr>
            ))}</tbody>
          </table>
        </div>
        {filtered.length === 0 && <div className="text-center py-10 text-stone-500">Inga kunder hittades</div>}
      </Card>

      {(showAdd || editId) && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" onClick={() => { setShowAdd(false); setEditId(null); }}>
          <Card className="w-full max-w-lg shadow-2xl" onClick={e => e.stopPropagation()}>
            <CardHeader><CardTitle>{editId ? 'Redigera kund' : 'Ny kund'}</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div><label className="block text-sm font-medium mb-1">Företag</label><Input value={form.companyName} onChange={e => setForm({ ...form, companyName: e.target.value })} /></div>
              <div className="grid grid-cols-2 gap-4"><div><label className="block text-sm font-medium mb-1">Kontaktperson</label><Input value={form.contactName} onChange={e => setForm({ ...form, contactName: e.target.value })} /></div><div><label className="block text-sm font-medium mb-1">E-post</label><Input value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} /></div></div>
              <div className="grid grid-cols-2 gap-4"><div><label className="block text-sm font-medium mb-1">Telefon</label><Input value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })} /></div><div><label className="block text-sm font-medium mb-1">Bransch</label><Input value={form.industry} onChange={e => setForm({ ...form, industry: e.target.value })} /></div></div>
              <div className="grid grid-cols-2 gap-4">
                <div><label className="block text-sm font-medium mb-1">Paket</label><select value={form.plan} onChange={e => setForm({ ...form, plan: e.target.value })} className="w-full h-9 rounded-md border border-stone-300 px-3 text-sm"><option>Bas</option><option>Pro</option><option>Premium</option></select></div>
                <div><label className="block text-sm font-medium mb-1">Status</label><select value={form.status} onChange={e => setForm({ ...form, status: e.target.value })} className="w-full h-9 rounded-md border border-stone-300 px-3 text-sm"><option value="active">Aktiv</option><option value="paused">Pausad</option><option value="cancelled">Avslutad</option></select></div>
              </div>
              <div><label className="block text-sm font-medium mb-1">Anteckningar</label><Textarea value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} rows={3} /></div>
              <div className="flex gap-3 pt-2"><Button onClick={saveCustomer} className="bg-blue-600 hover:bg-blue-700 text-white flex-1">{editId ? 'Spara ändringar' : 'Skapa kund'}</Button><Button variant="outline" onClick={() => { setShowAdd(false); setEditId(null); }}>Avbryt</Button></div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}

/* ─── Projects ─── */
function ProjectsSection({ projects, customers, onRefresh }: { projects: Project[]; customers: Customer[]; onRefresh: () => void }) {
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState({ customerId: '', name: '', description: '', status: 'planning' });

  const saveProject = async () => {
    await fetch('/api/projects', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...form, startDate: new Date().toISOString() }) });
    setShowAdd(false); setForm({ customerId: '', name: '', description: '', status: 'planning' }); onRefresh();
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-end"><Button onClick={() => setShowAdd(true)} className="bg-blue-600 hover:bg-blue-700 text-white"><Plus className="w-4 h-4 mr-2" />Nytt projekt</Button></div>
      <Card className="border-stone-200 overflow-hidden"><div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead><tr className="bg-stone-50 border-b border-stone-200"><th className="text-left px-4 py-3 font-medium text-stone-500">Projekt</th><th className="text-left px-4 py-3 font-medium text-stone-500">Kund</th><th className="text-left px-4 py-3 font-medium text-stone-500">Status</th><th className="text-left px-4 py-3 font-medium text-stone-500 hidden md:table-cell">Start</th><th className="text-right px-4 py-3 font-medium text-stone-500">Åtgärd</th></tr></thead>
          <tbody>{projects.map(p => (
            <tr key={p.id} className="border-b border-stone-100 hover:bg-stone-50"><td className="px-4 py-3 font-medium text-stone-900">{p.name}</td><td className="px-4 py-3 text-stone-600">{p.customer?.companyName || '—'}</td><td className="px-4 py-3"><Badge className={`${statusColors[p.status] || ''} text-xs`}>{statusLabels[p.status] || p.status}</Badge></td><td className="px-4 py-3 text-stone-500 hidden md:table-cell">{new Date(p.startDate).toLocaleDateString('sv-SE')}</td><td className="px-4 py-3 text-right"><button onClick={async () => { await fetch(`/api/projects/${p.id}`, { method: 'DELETE' }); onRefresh(); }} className="p-1 text-stone-400 hover:text-red-600"><Trash2 className="w-4 h-4" /></button></td></tr>
          ))}</tbody>
        </table>
      </div></Card>
      {showAdd && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" onClick={() => setShowAdd(false)}>
          <Card className="w-full max-w-lg shadow-2xl" onClick={e => e.stopPropagation()}>
            <CardHeader><CardTitle>Nytt projekt</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div><label className="block text-sm font-medium mb-1">Kund</label><select value={form.customerId} onChange={e => setForm({ ...form, customerId: e.target.value })} className="w-full h-9 rounded-md border border-stone-300 px-3 text-sm"><option value="">Välj kund...</option>{customers.filter(c => c.status === 'active').map(c => <option key={c.id} value={c.id}>{c.companyName}</option>)}</select></div>
              <div><label className="block text-sm font-medium mb-1">Projektnamn</label><Input value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} /></div>
              <div><label className="block text-sm font-medium mb-1">Beskrivning</label><Textarea value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} rows={3} /></div>
              <div><label className="block text-sm font-medium mb-1">Status</label><select value={form.status} onChange={e => setForm({ ...form, status: e.target.value })} className="w-full h-9 rounded-md border border-stone-300 px-3 text-sm"><option value="planning">Planering</option><option value="in_progress">Pågående</option><option value="review">Granskning</option><option value="completed">Klar</option></select></div>
              <div className="flex gap-3 pt-2"><Button onClick={saveProject} className="bg-blue-600 hover:bg-blue-700 text-white flex-1">Skapa projekt</Button><Button variant="outline" onClick={() => setShowAdd(false)}>Avbryt</Button></div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}

/* ─── Invoices ─── */
function InvoicesSection({ invoices, customers, onRefresh }: { invoices: Invoice[]; customers: Customer[]; onRefresh: () => void }) {
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState({ customerId: '', amount: '', description: '', dueDate: '' });

  const totalUnpaid = invoices.filter(i => i.status === 'pending' || i.status === 'overdue').reduce((s, i) => s + i.amount, 0);

  const saveInvoice = async () => {
    await fetch('/api/invoices', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ customerId: form.customerId, amount: parseFloat(form.amount), description: form.description, dueDate: new Date(form.dueDate).toISOString(), status: 'pending' }) });
    setShowAdd(false); setForm({ customerId: '', amount: '', description: '', dueDate: '' }); onRefresh();
  };

  const markPaid = async (id: string) => { await fetch(`/api/invoices/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status: 'paid', paidDate: new Date().toISOString() }) }); onRefresh(); };

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row gap-3 sm:items-center justify-between">
        <div className="text-stone-600">Obetalt: <span className="text-xl font-bold text-red-600">{totalUnpaid.toLocaleString('sv-SE')} kr</span></div>
        <Button onClick={() => setShowAdd(true)} className="bg-blue-600 hover:bg-blue-700 text-white"><Plus className="w-4 h-4 mr-2" />Ny faktura</Button>
      </div>
      <Card className="border-stone-200 overflow-hidden"><div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead><tr className="bg-stone-50 border-b border-stone-200"><th className="text-left px-4 py-3 font-medium text-stone-500">Beskrivning</th><th className="text-left px-4 py-3 font-medium text-stone-500">Kund</th><th className="text-left px-4 py-3 font-medium text-stone-500">Belopp</th><th className="text-left px-4 py-3 font-medium text-stone-500">Förfallo</th><th className="text-left px-4 py-3 font-medium text-stone-500">Status</th><th className="text-right px-4 py-3 font-medium text-stone-500">Åtgärd</th></tr></thead>
          <tbody>{invoices.map(inv => (
            <tr key={inv.id} className="border-b border-stone-100 hover:bg-stone-50"><td className="px-4 py-3 font-medium text-stone-900">{inv.description}</td><td className="px-4 py-3 text-stone-600">{inv.customer?.companyName || '—'}</td><td className="px-4 py-3 text-stone-900 font-medium">{inv.amount.toLocaleString('sv-SE')} kr</td><td className="px-4 py-3 text-stone-500">{new Date(inv.dueDate).toLocaleDateString('sv-SE')}</td><td className="px-4 py-3"><Badge className={`${statusColors[inv.status] || ''} text-xs`}>{statusLabels[inv.status] || inv.status}</Badge></td><td className="px-4 py-3 text-right">{inv.status !== 'paid' && <button onClick={() => markPaid(inv.id)} className="text-xs text-emerald-600 hover:text-emerald-800 font-medium">Markera betald</button>}</td></tr>
          ))}</tbody>
        </table>
      </div></Card>
      {showAdd && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" onClick={() => setShowAdd(false)}>
          <Card className="w-full max-w-lg shadow-2xl" onClick={e => e.stopPropagation()}>
            <CardHeader><CardTitle>Ny faktura</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div><label className="block text-sm font-medium mb-1">Kund</label><select value={form.customerId} onChange={e => setForm({ ...form, customerId: e.target.value })} className="w-full h-9 rounded-md border border-stone-300 px-3 text-sm"><option value="">Välj kund...</option>{customers.map(c => <option key={c.id} value={c.id}>{c.companyName}</option>)}</select></div>
              <div><label className="block text-sm font-medium mb-1">Belopp (kr)</label><Input type="number" value={form.amount} onChange={e => setForm({ ...form, amount: e.target.value })} /></div>
              <div><label className="block text-sm font-medium mb-1">Beskrivning</label><Input value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} /></div>
              <div><label className="block text-sm font-medium mb-1">Förfallodatum</label><Input type="date" value={form.dueDate} onChange={e => setForm({ ...form, dueDate: e.target.value })} /></div>
              <div className="flex gap-3 pt-2"><Button onClick={saveInvoice} className="bg-blue-600 hover:bg-blue-700 text-white flex-1">Skapa faktura</Button><Button variant="outline" onClick={() => setShowAdd(false)}>Avbryt</Button></div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}

/* ─── Messages ─── */
function MessagesSection({ messages, onRefresh }: { messages: ContactMsg[]; onRefresh: () => void }) {
  const toggleRead = async (m: ContactMsg) => { await fetch(`/api/contact/${m.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ read: !m.read }) }); onRefresh(); };
  const deleteMsg = async (id: string) => { await fetch(`/api/contact/${id}`, { method: 'DELETE' }); onRefresh(); };

  return (
    <div className="space-y-3">
      {messages.length === 0 && <Card className="border-stone-200"><CardContent className="py-10 text-center text-stone-500">Inga meddelanden</CardContent></Card>}
      {messages.map(m => (
        <Card key={m.id} className={`border-stone-200 transition-all ${!m.read ? 'border-l-4 border-l-blue-500 bg-blue-50/30' : ''}`}>
          <CardContent className="p-5">
            <div className="flex items-start justify-between gap-4">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 mb-1"><p className={`text-sm ${!m.read ? 'font-semibold text-stone-900' : 'text-stone-700'}`}>{m.name}</p>{m.company && <Badge variant="secondary" className="text-xs">{m.company}</Badge>}</div>
                <p className="text-xs text-stone-500 mb-2">{m.email}{m.phone ? ` · ${m.phone}` : ''} · {new Date(m.createdAt).toLocaleDateString('sv-SE')}</p>
                <p className="text-stone-600 text-sm leading-relaxed">{m.message}</p>
              </div>
              <div className="flex gap-1 shrink-0">
                <button onClick={() => toggleRead(m)} className="p-1.5 text-stone-400 hover:text-blue-600 rounded" title={m.read ? 'Markera oläst' : 'Markera läst'}>{m.read ? <Mail className="w-4 h-4" /> : <CheckCircle2 className="w-4 h-4" />}</button>
                <button onClick={() => deleteMsg(m.id)} className="p-1.5 text-stone-400 hover:text-red-600 rounded" title="Ta bort"><Trash2 className="w-4 h-4" /></button>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

/* ─── Settings ─── */
function SettingsSection() {
  const [currentPw, setCurrentPw] = useState('');
  const [newPw, setNewPw] = useState('');
  const [saved, setSaved] = useState(false);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    // Simplified — in production, verify current password and hash new one
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="max-w-md space-y-6">
      <Card className="border-stone-200"><CardHeader><CardTitle>Ändra lösenord</CardTitle></CardHeader><CardContent>
        <form onSubmit={handleSave} className="space-y-4">
          <div><label className="block text-sm font-medium mb-1">Nuvarande lösenord</label><Input type="password" value={currentPw} onChange={e => setCurrentPw(e.target.value)} /></div>
          <div><label className="block text-sm font-medium mb-1">Nytt lösenord</label><Input type="password" value={newPw} onChange={e => setNewPw(e.target.value)} /></div>
          <Button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white">{saved ? 'Sparat!' : 'Spara lösenord'}</Button>
        </form>
      </CardContent></Card>
    </div>
  );
}

/* ═══════════════════════════════════════════
   MAIN PAGE
   ═══════════════════════════════════════════ */
export default function Home() {
  const [view, setView] = useState<View>('landing');
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    // Check if session cookie exists
    const checkSession = async () => {
      try {
        const res = await fetch('/api/stats');
        if (res.ok) { setLoggedIn(true); } // If stats API works, we're authenticated
      } catch { /* not logged in */ }
    };
    // Don't auto-login, let user click login
  }, []);

  const handleLogin = () => { setLoggedIn(true); setView('dashboard'); };
  const handleLogout = () => { setLoggedIn(false); setView('landing'); document.cookie = 'ownli_session=; max-age=0; path=/'; };

  if (view === 'login') return <LoginPage onLogin={handleLogin} onBack={() => setView('landing')} />;
  if (view === 'dashboard' && loggedIn) return <Dashboard onLogout={handleLogout} />;
  return <LandingPage onLogin={() => setView('login')} />;
}
