'use client';

import { useState } from 'react';
import { Mail, Clock, Search, ArrowRight, CheckCircle2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import Navbar from '@/components/shared/Navbar';
import Footer from '@/components/shared/Footer';
import { useReveal } from '@/components/shared/hooks';

export default function KontaktPage() {
  const [contactSent, setContactSent] = useState(false);
  const leftRef = useReveal('reveal-left');
  const rightRef = useReveal('reveal-right');

  const handleContact = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    try {
      await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: fd.get('name'),
          email: fd.get('email'),
          phone: fd.get('phone'),
          company: fd.get('company'),
          message: fd.get('message'),
        }),
      });
      setContactSent(true);
      setTimeout(() => setContactSent(false), 4000);
      (e.target as HTMLFormElement).reset();
    } catch { /* silent */ }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main id="main-content" className="flex-1 pt-20">
        {/* Hero */}
        <section className="py-16 sm:py-24 bg-gradient-to-b from-stone-50 to-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl reveal-up-lg" ref={useReveal()}>
              <div className="mb-4 inline-flex items-center gap-2 text-blue-600 text-xs font-semibold tracking-[0.25em] uppercase font-[family-name:var(--font-display)]">
                <span className="h-px w-8 bg-blue-600/60" />Kontakt<span className="h-px w-8 bg-blue-600/60" />
              </div>
              <h1 className="text-4xl sm:text-6xl font-bold text-stone-900 mb-6 font-[family-name:var(--font-display)]">
                Redo att <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-cyan-500">synas online</span>?
              </h1>
              <p className="text-lg sm:text-xl text-stone-500 leading-relaxed">
                Berätta om ditt företag och vilka behov du har. Vi återkommer med ett förslag inom 24 timmar — helt kostnadsfritt.
              </p>
            </div>
          </div>
        </section>

        {/* Contact form + info */}
        <section className="py-16 sm:py-24 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-5 gap-16">
              <div className="lg:col-span-2 reveal-left" ref={leftRef}>
                <h2 className="text-3xl sm:text-4xl font-bold text-stone-900 mb-6 font-[family-name:var(--font-display)]">Kontakta oss</h2>
                <p className="text-lg text-stone-500 mb-10 leading-relaxed">Vi svarar på alla förfrågningar inom 24 timmar under vardagar. Ingen förpliktelse — bara ett samtal om hur vi kan hjälpa ditt företag.</p>
                <div className="space-y-6">
                  {[
                    { icon: Mail, t: 'E-post', d: 'hej@ownli.se' },
                    { icon: Clock, t: 'Svarstid', d: 'Inom 24 timmar vardagar' },
                    { icon: Search, t: 'Gratis konsultation', d: 'Vi analyserar din nuvarande närvaro' },
                  ].map(x => { const Icon = x.icon; return (
                    <div key={x.t} className="flex items-start gap-4">
                      <div className="w-12 h-12 rounded-xl bg-stone-100 flex items-center justify-center shrink-0"><Icon className="w-6 h-6 text-stone-700" /></div>
                      <div><p className="font-semibold text-stone-900 font-[family-name:var(--font-display)]">{x.t}</p><p className="text-stone-500">{x.d}</p></div>
                    </div>
                  ); })}
                </div>
              </div>
              <div className="lg:col-span-3 reveal-right" ref={rightRef}>
                <Card className="border-stone-200 shadow-lg shadow-stone-200/40">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-xl text-stone-900 font-[family-name:var(--font-display)]">Skicka förfrågan</CardTitle>
                    <p className="text-sm text-stone-500">Vi återkommer inom 24 timmar — kostnadsfritt.</p>
                  </CardHeader>
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
                      <Button type="submit" className="w-full bg-stone-900 hover:bg-stone-800 text-white rounded-full h-12 text-base shadow-lg active:scale-[0.97] transition-transform">
                        {contactSent ? (
                          <span className="flex items-center gap-2"><CheckCircle2 className="w-5 h-5" />Tack! Vi hör av oss snart.</span>
                        ) : (
                          <>Skicka förfrågan <ArrowRight className="w-4 h-4 ml-2" /></>
                        )}
                      </Button>
                    </form>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />

      <div className="fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-t border-stone-200 p-3 lg:hidden safe-area-bottom">
        <a href="#main-content">
          <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-full h-12 text-base shadow-lg active:scale-[0.97] transition-transform">
            Skicka förfrågan <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </a>
      </div>
    </div>
  );
}
