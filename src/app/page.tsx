'use client';

import { useState, useEffect } from 'react';
import {
  Globe,
  Mail,
  Shield,
  Smartphone,
  Zap,
  Clock,
  CheckCircle2,
  ArrowRight,
  Menu,
  X,
  ChevronRight,
  Star,
  UtensilsCrossed,
  Wifi,
  Server,
  Palette,
  Search,
  MessageCircle,
  BarChart3,
  Headphones,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

/* ──────────────────────────────────────────────
   NAVIGATION
   ────────────────────────────────────────────── */
function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const links = [
    { href: '#tjanster', label: 'Tjänster' },
    { href: '#priser', label: 'Priser' },
    { href: '#portfolio', label: 'Portfolio' },
    { href: '#process', label: 'Process' },
    { href: '#om-oss', label: 'Om oss' },
    { href: '#kontakt', label: 'Kontakt' },
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-white/95 backdrop-blur-md shadow-sm border-b border-stone-200'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">
          {/* Logo */}
          <a href="#" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-lg bg-amber-600 flex items-center justify-center">
              <UtensilsCrossed className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-stone-900 group-hover:text-amber-700 transition-colors">
              Rest<span className="text-amber-600">Web</span>
            </span>
          </a>

          {/* Desktop links */}
          <div className="hidden md:flex items-center gap-8">
            {links.map((l) => (
              <a
                key={l.href}
                href={l.href}
                className="text-sm font-medium text-stone-600 hover:text-amber-700 transition-colors"
              >
                {l.label}
              </a>
            ))}
            <a href="#kontakt">
              <Button className="bg-amber-600 hover:bg-amber-700 text-white rounded-full px-6">
                Kom igång
              </Button>
            </a>
          </div>

          {/* Mobile toggle */}
          <button
            className="md:hidden p-2 text-stone-700"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Meny"
          >
            {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden bg-white border-t border-stone-200 shadow-lg">
          <div className="px-4 py-4 space-y-3">
            {links.map((l) => (
              <a
                key={l.href}
                href={l.href}
                className="block py-2 text-stone-700 font-medium hover:text-amber-700"
                onClick={() => setMobileOpen(false)}
              >
                {l.label}
              </a>
            ))}
            <a href="#kontakt" onClick={() => setMobileOpen(false)}>
              <Button className="w-full bg-amber-600 hover:bg-amber-700 text-white rounded-full mt-2">
                Kom igång
              </Button>
            </a>
          </div>
        </div>
      )}
    </nav>
  );
}

/* ──────────────────────────────────────────────
   HERO
   ────────────────────────────────────────────── */
function Hero() {
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-stone-900 via-stone-800 to-amber-900" />
      <div
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage:
            'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.08\'%3E%3Ccircle cx=\'30\' cy=\'30\' r=\'2\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
        }}
      />
      <div className="absolute inset-0 bg-gradient-to-t from-stone-900/60 via-transparent to-transparent" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 sm:py-40">
        <div className="max-w-3xl">
          <Badge className="mb-6 bg-amber-600/20 text-amber-300 border-amber-500/30 hover:bg-amber-600/30 px-4 py-1.5 text-sm">
            <Wifi className="w-3.5 h-3.5 mr-1.5" />
            Specialiserade på restaurangbranschen
          </Badge>

          <h1 className="text-4xl sm:text-5xl lg:text-7xl font-bold text-white leading-tight mb-6">
            Din restaurang förtjänar en{' '}
            <span className="text-amber-400">fantastisk</span> hemsida
          </h1>

          <p className="text-lg sm:text-xl text-stone-300 mb-10 max-w-2xl leading-relaxed">
            Vi skapar vackra, snabba och säkra hemsidor för svenska restauranger.
            WordPress, .SE-domän, professionell e-post och hosting — allt i ett paket.
            Så att du kan fokusera på maten.
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <a href="#priser">
              <Button
                size="lg"
                className="bg-amber-600 hover:bg-amber-700 text-white rounded-full px-8 text-lg h-14 w-full sm:w-auto"
              >
                Se våra paket
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </a>
            <a href="#process">
              <Button
                size="lg"
                variant="outline"
                className="border-white/30 text-white hover:bg-white/10 rounded-full px-8 text-lg h-14 w-full sm:w-auto"
              >
                Så fungerar det
              </Button>
            </a>
          </div>

          {/* Trust indicators */}
          <div className="mt-14 flex flex-wrap gap-8 text-stone-400">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <span className="text-sm">.SE-domän ingår</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <span className="text-sm">SSL/HTTPS inkluderat</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <span className="text-sm">Svensk support</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <span className="text-sm">99.9% upptid</span>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 rounded-full border-2 border-white/30 flex items-start justify-center pt-2">
          <div className="w-1.5 h-3 rounded-full bg-white/50" />
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   SERVICES
   ────────────────────────────────────────────── */
const services = [
  {
    icon: Palette,
    title: 'Skräddarsydd design',
    description:
      'Unik och modern webbdesign anpassad efter din restaurangs profil och varumärke. Mobilanpassad, snabb och vacker — varje gång.',
  },
  {
    icon: Globe,
    title: '.SE-domän & hosting',
    description:
      'Vi ordnar din .SE-domän och lägger din hemsida på snabba och säkra servrar med 99.9% upptid. ChemiCloud WHM/cPanel för professionell drift.',
  },
  {
    icon: Mail,
    title: 'Professionell e-post',
    description:
      'info@dinrestaurang.se, bokning@dinrestaurang.se — e-post med SPF, DKIM och fullt spamskydd. Levereras varje gång.',
  },
  {
    icon: Shield,
    title: 'SSL & säkerhet',
    description:
      'Let&apos;s Encrypt SSL-certifikat, Imunify360 antivirusskydd, ModSecurity WAF och dagliga backuper. Din hemsida är säker hos oss.',
  },
  {
    icon: Smartphone,
    title: 'Mobilanpassad',
    description:
      '75% av dina besökare använder mobilen. Vi ser till att din hemsida ser fantastisk ut på alla skärmstorlekar — telefon, surfplatta och dator.',
  },
  {
    icon: BarChart3,
    title: 'SEO & statistik',
    description:
      'AWStats-trafikstatistik, Google-optimering och snabba laddningstider. Så att nya gäster hittar din restaurang på nätet.',
  },
];

function Services() {
  return (
    <section id="tjanster" className="py-20 sm:py-28 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <Badge className="mb-4 bg-amber-100 text-amber-800 border-amber-200">
            Våra tjänster
          </Badge>
          <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-4">
            Allt din restaurang behöver på nätet
          </h2>
          <p className="text-lg text-stone-600">
            Från domän och hosting till design och e-post — vi hanterar allt tekniskt
            så att du kan fokusera på att laga fantastisk mat.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          {services.map((s) => {
            const Icon = s.icon;
            return (
              <Card
                key={s.title}
                className="group border-stone-200 hover:border-amber-300 hover:shadow-lg transition-all duration-300"
              >
                <CardHeader>
                  <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center mb-3 group-hover:bg-amber-600 transition-colors">
                    <Icon className="w-6 h-6 text-amber-700 group-hover:text-white transition-colors" />
                  </div>
                  <CardTitle className="text-xl text-stone-900">{s.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-stone-600 leading-relaxed">{s.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   PRICING
   ────────────────────────────────────────────── */
const plans = [
  {
    name: 'Smakprov',
    price: '2 490',
    period: '/mån',
    setup: '5 990 kr upprättande',
    description: 'Perfekt för mindre restauranger som vill komma igång.',
    features: [
      'Snygg WordPress-hemsida',
      '.SE-domän ingår',
      '5 GB lagringsutrymme',
      '5 e-postkonton',
      'SSL/HTTPS',
      'Mobilanpassad',
      'Daglig backup',
      'E-postsupport',
    ],
    cta: 'Välj Smakprov',
    highlighted: false,
  },
  {
    name: 'Huvudrätt',
    price: '3 990',
    period: '/mån',
    setup: '9 990 kr upprättande',
    description: 'Vårt mest populära paket med allt du behöver.',
    features: [
      'Allt i Smakprov, plus:',
      '20 GB lagringsutrymme',
      '50 e-postkonton',
      'Online-meny & bordsbokning',
      'Google Maps-integration',
      'SEO-grundoptimering',
      'AWStats trafikstatistik',
      'Prioriterad support',
    ],
    cta: 'Välj Huvudrätt',
    highlighted: true,
  },
  {
    name: 'Dessert',
    price: '5 990',
    period: '/mån',
    setup: '14 990 kr upprättande',
    description: 'Premiumpaketet för restauranger som vill synas maximalt.',
    features: [
      'Allt i Huvudrätt, plus:',
      '50 GB lagringsutrymme',
      'Obegränsat e-postkonton',
      'Avancerad SEO-optimering',
      'Nyhetsbrev-integration',
      'Sociala medier-integration',
      'Prestandaoptimering',
      'Dedikerad kontaktperson',
    ],
    cta: 'Välj Dessert',
    highlighted: false,
  },
];

function Pricing() {
  return (
    <section id="priser" className="py-20 sm:py-28 bg-stone-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <Badge className="mb-4 bg-amber-100 text-amber-800 border-amber-200">
            Priser
          </Badge>
          <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-4">
            Transparenta priser — inga dolda kostnader
          </h2>
          <p className="text-lg text-stone-600">
            Välj det paket som passar din restaurang. Alla priser är exkl. moms.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan) => (
            <Card
              key={plan.name}
              className={`relative flex flex-col ${
                plan.highlighted
                  ? 'border-2 border-amber-500 shadow-xl shadow-amber-500/10 scale-[1.02]'
                  : 'border-stone-200'
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <Badge className="bg-amber-600 text-white px-4 py-1 text-sm">
                    Mest populär
                  </Badge>
                </div>
              )}
              <CardHeader className="pb-2">
                <CardTitle className="text-2xl text-stone-900">{plan.name}</CardTitle>
                <p className="text-stone-500 text-sm">{plan.description}</p>
              </CardHeader>
              <CardContent className="flex-1">
                <div className="mb-6">
                  <span className="text-4xl font-bold text-stone-900">{plan.price}</span>
                  <span className="text-stone-500">{plan.period}</span>
                  <p className="text-xs text-stone-400 mt-1">{plan.setup}</p>
                </div>
                <ul className="space-y-3">
                  {plan.features.map((f, i) => (
                    <li key={i} className="flex items-start gap-2.5">
                      <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                      <span className="text-sm text-stone-700">{f}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              <CardFooter>
                <a href="#kontakt" className="w-full">
                  <Button
                    className={`w-full rounded-full h-12 text-base font-medium ${
                      plan.highlighted
                        ? 'bg-amber-600 hover:bg-amber-700 text-white'
                        : 'bg-stone-900 hover:bg-stone-800 text-white'
                    }`}
                  >
                    {plan.cta}
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </a>
              </CardFooter>
            </Card>
          ))}
        </div>

        <p className="text-center text-stone-500 mt-10 text-sm">
          Alla paket inkluderar: ChemiCloud WHM/cPanel hosting, Let&apos;s Encrypt SSL,
          Imunify360 antivirusskydd, dagliga backuper (30 dagar), CloudLinux serverstabilitet
          och LiteSpeed webbserver för maximal prestanda.
        </p>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   PORTFOLIO
   ────────────────────────────────────────────── */
const portfolioItems = [
  {
    name: 'Trattoria Bella',
    type: 'Italiensk restaurang',
    location: 'Stockholm',
    features: ['Online-meny', 'Bordsbokning', 'Catering-sida'],
  },
  {
    name: 'Sjömagasinet',
    type: 'Fisk & skaldjur',
    location: 'Göteborg',
    features: ['Event-kalender', 'Galleri', 'Nyhetsbrev'],
  },
  {
    name: 'Kök & Bar',
    type: 'Modern svensk',
    location: 'Malmö',
    features: ['Lunchmeny', 'Dryckeslista', 'Instagram-feed'],
  },
  {
    name: 'Wok House',
    type: 'Asiatisk fusion',
    location: 'Uppsala',
    features: ['Takeaway-beställning', 'Allergi-info', 'Recensioner'],
  },
  {
    name: 'Bakgården Café',
    type: 'Café & brunch',
    location: 'Lund',
    features: ['Brunch-meny', 'Fotogalleri', 'Öppettider'],
  },
  {
    name: 'Grill & Vin',
    type: 'Steakhouse',
    location: 'Umeå',
    features: ['Vinlista', 'Bordsbokning', 'Presentkort'],
  },
];

function Portfolio() {
  return (
    <section id="portfolio" className="py-20 sm:py-28 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <Badge className="mb-4 bg-amber-100 text-amber-800 border-amber-200">
            Portfolio
          </Badge>
          <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-4">
            Restauranger som redan syns online
          </h2>
          <p className="text-lg text-stone-600">
            Några exempel på hur vi hjälper svenska restauranger att ta sin närvaro
            på nätet till nästa nivå.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {portfolioItems.map((item) => (
            <Card
              key={item.name}
              className="group overflow-hidden border-stone-200 hover:shadow-lg transition-all duration-300"
            >
              <div className="h-48 bg-gradient-to-br from-amber-100 via-stone-100 to-amber-50 relative flex items-center justify-center">
                <UtensilsCrossed className="w-16 h-16 text-amber-300 group-hover:text-amber-500 transition-colors" />
                <div className="absolute top-3 right-3">
                  <Badge className="bg-white/90 text-stone-700 text-xs">{item.location}</Badge>
                </div>
              </div>
              <CardHeader className="pb-2">
                <CardTitle className="text-lg text-stone-900">{item.name}</CardTitle>
                <p className="text-sm text-amber-700 font-medium">{item.type}</p>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-1.5">
                  {item.features.map((f) => (
                    <Badge
                      key={f}
                      variant="secondary"
                      className="bg-stone-100 text-stone-600 text-xs"
                    >
                      {f}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   PROCESS
   ────────────────────────────────────────────── */
const steps = [
  {
    num: '01',
    icon: MessageCircle,
    title: 'Vi pratar',
    text: 'Du berättar om din restaurang, din vision och vad du behöver. Vi lyssnar och ger råd om vilken lösning som passar bäst.',
  },
  {
    num: '02',
    icon: Palette,
    title: 'Vi designar',
    text: 'Vi skapar en unik design som speglar din restaurangs identitet. Du får se förslag och kan komma med justeringar tills du är nöjd.',
  },
  {
    num: '03',
    icon: Server,
    title: 'Vi bygger',
    text: 'Vi bygger din hemsida i WordPress, ordnar .SE-domän, e-post, SSL och hosting. Allt tekniskt sköter vi åt dig.',
  },
  {
    num: '04',
    icon: Zap,
    title: 'Vi lanserar',
    text: 'När du godkänt allt publicerar vi din nya hemsida. Därefter står vi för drift, underhåll och support — månadsvis.',
  },
];

function Process() {
  return (
    <section id="process" className="py-20 sm:py-28 bg-stone-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <Badge className="mb-4 bg-amber-600/20 text-amber-300 border-amber-500/30">
            Vår process
          </Badge>
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Från samtal till lansering — fyra enkla steg
          </h2>
          <p className="text-lg text-stone-400">
            Vi gör det enkelt. Du slipper tekniska detaljer och kan fokusera på
            det du gör bäst — att driva din restaurang.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((s) => {
            const Icon = s.icon;
            return (
              <div key={s.num} className="relative text-center">
                <div className="text-6xl font-black text-amber-600/20 mb-2">{s.num}</div>
                <div className="w-14 h-14 rounded-2xl bg-amber-600/20 flex items-center justify-center mx-auto mb-4">
                  <Icon className="w-7 h-7 text-amber-400" />
                </div>
                <h3 className="text-xl font-bold mb-3">{s.title}</h3>
                <p className="text-stone-400 leading-relaxed">{s.text}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   STATS BAR
   ────────────────────────────────────────────── */
function StatsBar() {
  const stats = [
    { value: '99.9%', label: 'Upptid' },
    { value: '< 2s', label: 'Laddtid' },
    { value: '24/7', label: 'Övervakning' },
    { value: '30 dag', label: 'Backup-historik' },
  ];
  return (
    <section className="py-12 bg-amber-600">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center text-white">
          {stats.map((s) => (
            <div key={s.label}>
              <div className="text-3xl sm:text-4xl font-bold">{s.value}</div>
              <div className="text-amber-200 text-sm mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   TESTIMONIALS
   ────────────────────────────────────────────── */
const testimonials = [
  {
    name: 'Marco Rossi',
    role: 'Ägare, Trattoria Bella',
    text: 'Äntligen en hemsida som vi är stolta över! Våra gäster hittar oss enkelt och bordsbokningarna har ökat med 40% sedan vi bytte till RestWeb.',
    stars: 5,
  },
  {
    name: 'Linda Johansson',
    role: 'Krögare, Sjömagasinet',
    text: 'Som restaurangägare har jag ingen tid med teknik. RestWeb sköter allt och deras support är fantastisk. Jag bara ringer och de fixar det.',
    stars: 5,
  },
  {
    name: 'Chen Wei',
    role: 'Ägare, Wok House',
    text: 'Vår takeaway-beställning online har revolutionerat vår verksamhet. Kunden beställer direkt på hemsidan — inga appar, inga mellanhänder.',
    stars: 5,
  },
];

function Testimonials() {
  return (
    <section className="py-20 sm:py-28 bg-stone-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <Badge className="mb-4 bg-amber-100 text-amber-800 border-amber-200">
            Kundröster
          </Badge>
          <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-4">
            Vad våra restauranger säger
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((t) => (
            <Card key={t.name} className="border-stone-200">
              <CardHeader>
                <div className="flex gap-0.5 mb-2">
                  {Array.from({ length: t.stars }).map((_, i) => (
                    <Star key={i} className="w-5 h-5 fill-amber-400 text-amber-400" />
                  ))}
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-stone-700 leading-relaxed italic mb-4">&ldquo;{t.text}&rdquo;</p>
                <div>
                  <p className="font-semibold text-stone-900">{t.name}</p>
                  <p className="text-sm text-stone-500">{t.role}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   ABOUT
   ────────────────────────────────────────────── */
function About() {
  return (
    <section id="om-oss" className="py-20 sm:py-28 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <Badge className="mb-4 bg-amber-100 text-amber-800 border-amber-200">
              Om oss
            </Badge>
            <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-6">
              Vi förstår restaurangbranschen — och webben
            </h2>
            <div className="space-y-4 text-stone-600 leading-relaxed">
              <p>
                RestWeb grundades med en enkel idé: svenska restauranger förtjänar
                bättre hemsidor. För ofta ser vi vackra restauranger med dåliga,
                långsamma eller osäkra hemsidor som kostar för mycket.
              </p>
              <p>
                Vi kombinerar djup teknisk expertis inom WordPress, hosting och
                webbsäkerhet med en genuin förståelse för restaurangbranschens
                unika behov — online-menyer, bordsbokning, catering-formulär och
                smakrik presentation.
              </p>
              <p>
                Vår infrastruktur bygger på ChemiCloud WHM/cPanel hosting med
                CloudLinux, LiteSpeed och Imunify360 — samma teknik som stora
                webbhotell använder, men med personlig service och restaurangfokus.
              </p>
            </div>
            <div className="mt-8 flex flex-wrap gap-6">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
                  <Shield className="w-5 h-5 text-amber-700" />
                </div>
                <div>
                  <p className="font-semibold text-stone-900 text-sm">Säker hosting</p>
                  <p className="text-xs text-stone-500">ChemiCloud + Imunify360</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
                  <Globe className="w-5 h-5 text-amber-700" />
                </div>
                <div>
                  <p className="font-semibold text-stone-900 text-sm">.SE-domäner</p>
                  <p className="text-xs text-stone-500">Via certifierade registrarer</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
                  <Headphones className="w-5 h-5 text-amber-700" />
                </div>
                <div>
                  <p className="font-semibold text-stone-900 text-sm">Svensk support</p>
                  <p className="text-xs text-stone-500">Personlig & snabb</p>
                </div>
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="aspect-[4/3] rounded-2xl bg-gradient-to-br from-amber-200 via-amber-100 to-stone-200 flex items-center justify-center">
              <div className="text-center p-8">
                <Server className="w-20 h-20 text-amber-600 mx-auto mb-4" />
                <p className="text-amber-800 font-semibold text-lg">Professionell infrastruktur</p>
                <p className="text-amber-700 text-sm mt-1">WHM/cPanel · LiteSpeed · CloudLinux</p>
              </div>
            </div>
            <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-amber-600 rounded-2xl flex items-center justify-center text-white shadow-lg">
              <div className="text-center">
                <div className="text-3xl font-bold">5+</div>
                <div className="text-xs text-amber-200">Års erfarenhet</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   FAQ
   ────────────────────────────────────────────── */
const faqs = [
  {
    q: 'Hur lång tid tar det att få en hemsida?',
    a: 'Normalt 2–4 veckor från att vi startar till att hemsidan är live. Enklare projekt kan gå snabbare.',
  },
  {
    q: 'Kan jag flytta min befintliga hemsida till er?',
    a: 'Absolut! Vi migrerar din befintliga WordPress-hemsida utan driftavbrott via WHM Transfer Tool.',
  },
  {
    q: 'Vad händer om jag vill säga upp mitt abonnemang?',
    a: 'Du kan säga upp när som helst med 30 dagars varsel. Du äger alltid din domän och din webbplats.',
  },
  {
    q: 'Ingår uppdateringar av hemsidan?',
    a: 'Ja, WordPress, teman och plugins uppdateras automatiskt via vår WP Toolkit. Mindre textändringar gör vi utan extra kostnad.',
  },
  {
    q: 'Får jag tillgång till cPanel?',
    a: 'Ja, du får full tillgång till cPanel där du kan hantera e-post, filer, databaser och mer. Vi hjälper gärna till om det behövs.',
  },
  {
    q: 'Varför .SE-domän och inte .com?',
    a: 'För svenska restauranger signalerar .SE lokalt förtroende och förbättrar synligheten i svenska sökresultat. Vi rekommenderar alltid .SE som primär domän.',
  },
];

function FAQ() {
  const [open, setOpen] = useState<number | null>(null);

  return (
    <section className="py-20 sm:py-28 bg-stone-50">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-amber-100 text-amber-800 border-amber-200">Vanliga frågor</Badge>
          <h2 className="text-3xl sm:text-4xl font-bold text-stone-900">
            Frågor och svar
          </h2>
        </div>

        <div className="space-y-3">
          {faqs.map((faq, i) => (
            <div
              key={i}
              className="bg-white rounded-xl border border-stone-200 overflow-hidden"
            >
              <button
                className="w-full px-6 py-5 text-left flex items-center justify-between gap-4 hover:bg-stone-50 transition-colors"
                onClick={() => setOpen(open === i ? null : i)}
              >
                <span className="font-medium text-stone-900">{faq.q}</span>
                <ChevronRight
                  className={`w-5 h-5 text-stone-400 shrink-0 transition-transform duration-200 ${
                    open === i ? 'rotate-90' : ''
                  }`}
                />
              </button>
              {open === i && (
                <div className="px-6 pb-5 text-stone-600 leading-relaxed">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   CONTACT
   ────────────────────────────────────────────── */
function Contact() {
  const [sent, setSent] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSent(true);
    setTimeout(() => setSent(false), 4000);
  };

  return (
    <section id="kontakt" className="py-20 sm:py-28 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16">
          {/* Left: Info */}
          <div>
            <Badge className="mb-4 bg-amber-100 text-amber-800 border-amber-200">Kontakt</Badge>
            <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-6">
              Redo att synas online?
            </h2>
            <p className="text-lg text-stone-600 mb-10 leading-relaxed">
              Berätta om din restaurang och vilka behov du har. Vi återkommer med
              ett förslag inom 24 timmar — helt kostnadsfritt och utan förpliktelser.
            </p>

            <div className="space-y-6">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center shrink-0">
                  <Mail className="w-6 h-6 text-amber-700" />
                </div>
                <div>
                  <p className="font-semibold text-stone-900">E-post</p>
                  <p className="text-stone-600">hej@restweb.se</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center shrink-0">
                  <Clock className="w-6 h-6 text-amber-700" />
                </div>
                <div>
                  <p className="font-semibold text-stone-900">Svarstid</p>
                  <p className="text-stone-600">Inom 24 timmar vardagar</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center shrink-0">
                  <Search className="w-6 h-6 text-amber-700" />
                </div>
                <div>
                  <p className="font-semibold text-stone-900">Obligatorisk konsultation</p>
                  <p className="text-stone-600">Vi analyserar din nuvarande närvaro gratis</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right: Form */}
          <Card className="border-stone-200">
            <CardHeader>
              <CardTitle className="text-xl text-stone-900">Skicka förfrågan</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                  <label className="block text-sm font-medium text-stone-700 mb-1.5">
                    Restaurangens namn
                  </label>
                  <Input
                    placeholder="T.ex. Trattoria Bella"
                    className="h-11 border-stone-300"
                    required
                  />
                </div>
                <div className="grid sm:grid-cols-2 gap-5">
                  <div>
                    <label className="block text-sm font-medium text-stone-700 mb-1.5">
                      Ditt namn
                    </label>
                    <Input
                      placeholder="För- och efternamn"
                      className="h-11 border-stone-300"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-stone-700 mb-1.5">
                      E-post
                    </label>
                    <Input
                      type="email"
                      placeholder="namn@restaurang.se"
                      className="h-11 border-stone-300"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-stone-700 mb-1.5">
                    Telefon
                  </label>
                  <Input
                    type="tel"
                    placeholder="070-123 45 67"
                    className="h-11 border-stone-300"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-stone-700 mb-1.5">
                    Berätta om din restaurang
                  </label>
                  <Textarea
                    placeholder="Vilken typ av restaurang har du? Vad behöver du för funktioner på hemsidan? Har du redan en domän?"
                    className="border-stone-300 min-h-[120px]"
                  />
                </div>
                <Button
                  type="submit"
                  className="w-full bg-amber-600 hover:bg-amber-700 text-white rounded-full h-12 text-base"
                >
                  {sent ? 'Tack! Vi hör av oss snart.' : 'Skicka förfrågan'}
                  {!sent && <ArrowRight className="w-4 h-4 ml-2" />}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   FOOTER
   ────────────────────────────────────────────── */
function Footer() {
  return (
    <footer className="bg-stone-900 text-stone-400 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-10">
          {/* Brand */}
          <div className="sm:col-span-2 lg:col-span-1">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 rounded-lg bg-amber-600 flex items-center justify-center">
                <UtensilsCrossed className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">
                Rest<span className="text-amber-400">Web</span>
              </span>
            </div>
            <p className="text-sm leading-relaxed">
              Professionella hemsidor för svenska restauranger. Design, hosting, domän och e-post — allt i ett.
            </p>
          </div>

          {/* Tjänster */}
          <div>
            <h4 className="text-white font-semibold mb-3">Tjänster</h4>
            <ul className="space-y-2 text-sm">
              <li>Webbdesign</li>
              <li>WordPress</li>
              <li>.SE-domän</li>
              <li>E-post</li>
              <li>Hosting</li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h4 className="text-white font-semibold mb-3">Support</h4>
            <ul className="space-y-2 text-sm">
              <li>Vanliga frågor</li>
              <li>cPanel-guide</li>
              <li>WordPress-hjälp</li>
              <li>Driftstatus</li>
            </ul>
          </div>

          {/* Kontakt */}
          <div>
            <h4 className="text-white font-semibold mb-3">Kontakt</h4>
            <ul className="space-y-2 text-sm">
              <li>hej@restweb.se</li>
              <li>Mån–Fre 09–17</li>
              <li>Sverige</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-stone-800 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-sm">&copy; 2026 RestWeb. Alla rättigheter förbehållna.</p>
          <div className="flex gap-6 text-sm">
            <span className="hover:text-amber-400 cursor-pointer transition-colors">Integritetspolicy</span>
            <span className="hover:text-amber-400 cursor-pointer transition-colors">Villkor</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

/* ──────────────────────────────────────────────
   PAGE
   ────────────────────────────────────────────── */
export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Hero />
        <Services />
        <Pricing />
        <Portfolio />
        <Process />
        <StatsBar />
        <Testimonials />
        <About />
        <FAQ />
        <Contact />
      </main>
      <Footer />
    </div>
  );
}
