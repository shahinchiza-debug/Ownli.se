'use client';

import { useState } from 'react';
import { CheckCircle2, ArrowRight, ChevronRight } from 'lucide-react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import Navbar from '@/components/shared/Navbar';
import Footer from '@/components/shared/Footer';
import { useReveal } from '@/components/shared/hooks';
import Link from 'next/link';

const purchaseOptions = [
  { name: 'Direktköp', price: '35 000', unit: 'kr', desc: 'Kunden köper hemsidan direkt och äger den fullt ut från dag ett.', features: ['Full äganderätt från dag 1', 'Drift och hosting väljs fritt', 'Ingen bindningstid', 'All kod och material tillhör dig', 'Fri att flytta när du vill'], highlighted: false },
  { name: 'Avbetalning 2 år', price: '2 000', unit: 'kr/månaden', desc: 'Hemsidan betalas av under 24 månader, varefter full äganderätt övergår till kunden.', features: ['Betalning över 24 månader', 'Hosting, drift och support ingår', '1 större omfaktorering ingår', 'Full äganderätt efter perioden', 'Välj driftpartner fritt efteråt'], highlighted: true },
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

export default function PriserPage() {
  const heroRef = useReveal();
  const cardsRef = useReveal();
  const faqRef = useReveal('reveal-blur');
  const [faqOpen, setFaqOpen] = useState<number | null>(null);

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main id="main-content" className="flex-1 pt-20">
        {/* Hero */}
        <section className="py-16 sm:py-24 bg-gradient-to-b from-stone-50 to-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto text-center reveal-up-lg" ref={heroRef}>
              <div className="mb-4 inline-flex items-center gap-2 text-blue-600 text-xs font-semibold tracking-[0.25em] uppercase font-[family-name:var(--font-display)]">
                <span className="h-px w-8 bg-blue-600/60" />Priser<span className="h-px w-8 bg-blue-600/60" />
              </div>
              <h1 className="text-4xl sm:text-6xl font-bold text-stone-900 mb-6 font-[family-name:var(--font-display)]">
                Transparenta <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-cyan-500">priser</span>
              </h1>
              <p className="text-lg sm:text-xl text-stone-500 leading-relaxed">Du äger, vi bygger. Alla priser exkl. moms.</p>
            </div>
          </div>
        </section>

        {/* Pricing cards */}
        <section className="py-16 sm:py-24 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto stagger-scale" ref={cardsRef}>
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
                    <ul className="space-y-3.5">
                      {opt.features.map((f, i) => (
                        <li key={i} className="flex items-start gap-3">
                          <div className="mt-0.5 w-5 h-5 rounded-full bg-emerald-50 flex items-center justify-center shrink-0">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                          </div>
                          <span className="text-sm text-stone-700 leading-relaxed">{f}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                  <CardFooter className="pt-4 pb-6">
                    <Link href="/kontakt" className="w-full">
                      <Button className={`w-full rounded-full h-12 text-base font-medium transition-all active:scale-[0.97] ${opt.highlighted ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/25' : 'bg-stone-900 hover:bg-stone-800 text-white'}`}>
                        Välj {opt.name} <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                    </Link>
                  </CardFooter>
                </Card>
              ))}
            </div>

            {/* How it works */}
            <div className="mt-20 bg-stone-50 rounded-2xl p-8 sm:p-12 max-w-4xl mx-auto">
              <h3 className="text-2xl font-bold text-stone-900 mb-6 text-center font-[family-name:var(--font-display)]">Hur det fungerar</h3>
              <div className="space-y-4 text-stone-600 leading-relaxed">
                <p>Du köper din hemsida via ett av två alternativ. Vid <strong className="text-stone-900">direktköp</strong> betalar du 35 000 kr och äger hemsidan fullt ut från dag ett — fri att hosta hos oss, hos någon annan eller på egen hand.</p>
                <p>Vid <strong className="text-stone-900">avbetalning 2 år</strong> betalar du 2 000 kr per månad i 24 månader. Under perioden ingår drift, support och en större omfaktorering. När perioden är slut övergår full äganderätt till dig.</p>
                <p><strong className="text-stone-900">Du äger alltid din domän och din kod.</strong> Vi bygger, du bestämmer — precis som varumärket lovar.</p>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="py-16 sm:py-24 bg-stone-50">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16 reveal-blur" ref={faqRef}>
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
