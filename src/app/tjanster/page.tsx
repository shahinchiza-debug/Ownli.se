'use client';

import { Globe, Mail, Shield, Smartphone, BarChart3, Palette, ArrowRight, CheckCircle2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import Navbar from '@/components/shared/Navbar';
import Footer from '@/components/shared/Footer';
import { useReveal } from '@/components/shared/hooks';
import Link from 'next/link';

const services = [
  {
    icon: Palette,
    title: 'Skräddarsydd design',
    desc: 'Unik och modern webbdesign anpassad efter ditt företags profil och varumärke. Mobilanpassad, snabb och vacker — varje gång.',
    details: [
      'Egen design från grunden — inga färdiga mallar',
      'Responsiv för mobil, surfplatta och dator',
      'Anpassad färgpalett och typografi efter din profil',
      'Snabb laddning med optimerad kod',
      'Tillgänglighetsanpassad enligt WCAG',
    ],
  },
  {
    icon: Globe,
    title: '.SE-domän & hosting',
    desc: 'Vi ordnar din .SE-domän och lägger din hemsida på snabba och säkra servrar med 99.9% upptid. WHM/cPanel för professionell drift.',
    details: [
      'Registrering av .SE-domän i ditt namn',
      'Professionell hosting med LiteSpeed-webbserver',
      'CloudLinux för isolerad och stabil drift',
      'WHM/cPanel för enkel administration',
      '99.9% garanterad upptid',
    ],
  },
  {
    icon: Mail,
    title: 'Professionell e-post',
    desc: 'info@dittforetag.se, kontakt@dittforetag.se — e-post med SPF, DKIM och fullt spamskydd. Levereras varje gång.',
    details: [
      'E-post i ditt domännamn (info@, kontakt@, namn@)',
      'SPF och DKIM för maximal leveranssäkerhet',
      'Imunify360 antivirusskydd',
      'Webbmail, IMAP och SMTP-åtkomst',
      'Automatiskt spamskydd med SpamAssassin',
    ],
  },
  {
    icon: Shield,
    title: 'SSL & säkerhet',
    desc: "Let's Encrypt SSL-certifikat, Imunify360 antivirusskydd, ModSecurity WAF och dagliga backuper. Din hemsida är säker hos oss.",
    details: [
      "Gratis Let's Encrypt SSL-certifikat (HTTPS)",
      'Imunify360 realtidsskydd mot malware',
      'ModSecurity WAF (Web Application Firewall)',
      'Dagliga automatiska backuper (30 dagars historik)',
      'DDOS-skydd och intrångsdetektering',
    ],
  },
  {
    icon: Smartphone,
    title: 'Mobilanpassad',
    desc: '75% av dina besökare använder mobilen. Vi ser till att din hemsida ser fantastisk ut på alla skärmstorlekar — telefon, surfplatta och dator.',
    details: [
      'Touch-optimerade knappar och menyer',
      'Responsiv layout som anpassar sig automatiskt',
      'Snabb laddning även på mobilnät',
      'Testad på alla vanliga enheter och webbläsare',
      'Sticky mobil-CTA för maximal konvertering',
    ],
  },
  {
    icon: BarChart3,
    title: 'SEO & statistik',
    desc: 'AWStats-trafikstatistik, Google-optimering och snabba laddningstider. Så att nya kunder hittar ditt företag på nätet.',
    details: [
      'Sökmotoroptimerad kod och struktur',
      'AWStats och cPanel-trafikstatistik',
      'Snabba laddningstider (< 2 sekunder)',
      'Meta-taggar och Open Graph-optimering',
      'Sitemap.xml och robots.txt ingår',
    ],
  },
];

export default function TjansterPage() {
  const heroRef = useReveal();
  const gridRef = useReveal();

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main id="main-content" className="flex-1 pt-20">
        {/* Hero */}
        <section className="py-16 sm:py-24 bg-gradient-to-b from-stone-50 to-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl reveal-up-lg" ref={heroRef}>
              <div className="mb-4 inline-flex items-center gap-2 text-blue-600 text-xs font-semibold tracking-[0.25em] uppercase font-[family-name:var(--font-display)]">
                <span className="h-px w-8 bg-blue-600/60" />Tjänster<span className="h-px w-8 bg-blue-600/60" />
              </div>
              <h1 className="text-4xl sm:text-6xl font-bold text-stone-900 mb-6 font-[family-name:var(--font-display)]">
                Allt ditt företag behöver <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-cyan-500">på nätet</span>
              </h1>
              <p className="text-lg sm:text-xl text-stone-500 leading-relaxed mb-8">
                Från domän och hosting till design och e-post — vi hanterar allt tekniskt så att du kan fokusera på din verksamhet. Se nedan vad som ingår när du väljer Ownli.
              </p>
              <Link href="/priser">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-8 h-12 text-base shadow-lg shadow-blue-600/25 active:scale-[0.97] transition-transform">
                  Se våra priser <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Services detail */}
        <section className="py-16 sm:py-24 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16 stagger-children" ref={gridRef}>
            {services.map((s, i) => {
              const Icon = s.icon;
              const isEven = i % 2 === 0;
              return (
                <div key={s.title} className={`grid lg:grid-cols-2 gap-12 items-center ${!isEven ? 'lg:direction-rtl' : ''}`}>
                  <div className={!isEven ? 'lg:order-2' : ''}>
                    <div className="w-14 h-14 rounded-2xl bg-stone-100 flex items-center justify-center mb-5 group-hover:bg-stone-900 transition-all duration-300">
                      <Icon className="w-7 h-7 text-blue-600" />
                    </div>
                    <h2 className="text-2xl sm:text-3xl font-bold text-stone-900 mb-4 font-[family-name:var(--font-display)]">{s.title}</h2>
                    <p className="text-stone-500 leading-relaxed text-lg mb-6">{s.desc}</p>
                    <Link href="/kontakt">
                      <Button variant="outline" className="rounded-full border-stone-300 hover:border-stone-900 hover:bg-stone-900 hover:text-white transition-all">
                        Beställ {s.title.toLowerCase()} <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                    </Link>
                  </div>
                  <div className={!isEven ? 'lg:order-1' : ''}>
                    <Card className="border-stone-200 shadow-lg shadow-stone-100/50">
                      <CardHeader>
                        <CardTitle className="text-lg text-stone-900 font-[family-name:var(--font-display)]">Vad som ingår</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <ul className="space-y-3">
                          {s.details.map((d, j) => (
                            <li key={j} className="flex items-start gap-3">
                              <div className="mt-0.5 w-5 h-5 rounded-full bg-emerald-50 flex items-center justify-center shrink-0">
                                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                              </div>
                              <span className="text-sm text-stone-700 leading-relaxed">{d}</span>
                            </li>
                          ))}
                        </ul>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 sm:py-20 bg-stone-900 text-white">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4 font-[family-name:var(--font-display)]">Redo att komma igång?</h2>
            <p className="text-stone-400 text-lg mb-8">Vi bygger din hemsida — du äger den. Kontakta oss idag för en kostnadsfri konsultation.</p>
            <Link href="/kontakt">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-8 h-12 text-base shadow-lg shadow-blue-600/25 active:scale-[0.97] transition-transform">
                Kontakta oss <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
          </div>
        </section>
      </main>

      <Footer />

      {/* Mobile sticky CTA */}
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
