import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';

export async function POST() {
  try {
    const existing = await db.user.findFirst();
    if (existing) {
      return NextResponse.json({ error: 'Admin redan skapad' }, { status: 400 });
    }

    const hashedPassword = await bcrypt.hash('admin123', 10);
    const user = await db.user.create({
      data: { email: 'admin@webpro.se', name: 'Admin', password: hashedPassword, role: 'admin' },
    });

    // Seed demo customers
    const customers = await Promise.all([
      db.customer.create({ data: { companyName: 'Trattoria Bella', contactName: 'Marco Rossi', email: 'marco@trattoriabella.se', phone: '070-111 22 33', industry: 'Restaurang & café', plan: 'Pro', status: 'active', notes: 'Italiensk restaurang i Stockholm' } }),
      db.customer.create({ data: { companyName: 'Nordbygg AB', contactName: 'Emma Lindqvist', email: 'emma@nordbygg.se', phone: '070-222 33 44', industry: 'Hantverkare & bygg', plan: 'Premium', status: 'active', notes: 'Byggföretag med portfolio-behov' } }),
      db.customer.create({ data: { companyName: 'Hälsokällan', contactName: 'Sara Ahmed', email: 'sara@halsokallan.se', phone: '070-333 44 55', industry: 'Hälsa & vård', plan: 'Pro', status: 'active', notes: 'Klinik med bokningssystem' } }),
      db.customer.create({ data: { companyName: 'Juridikpartner KB', contactName: 'Anders Berg', email: 'anders@juridikpartner.se', phone: '070-444 55 66', industry: 'Juridik & ekonomi', plan: 'Bas', status: 'paused', notes: 'Pausat abonnemang t.o.m. sept' } }),
      db.customer.create({ data: { companyName: 'Svenska E-handel AB', contactName: 'Lisa Wang', email: 'lisa@sehandel.se', phone: '070-555 66 77', industry: 'Handel & e-handel', plan: 'Premium', status: 'active', notes: 'Webbutik i uppstart' } }),
      db.customer.create({ data: { companyName: 'Lärling Utbildning', contactName: 'Pär Svensson', email: 'par@larlingutbildning.se', phone: '070-678 90 12', industry: 'Utbildning', plan: 'Pro', status: 'cancelled', notes: 'Utbildningsföretag. Avslutat abonnemang.' } }),
    ]);

    // Seed demo projects
    await Promise.all([
      db.project.create({ data: { customerId: customers[0].id, name: 'Trattoria Bella — Ny hemsida', description: 'Komplett nybyggnad av hemsida med online-meny', status: 'completed', startDate: new Date('2025-01-15'), endDate: new Date('2025-02-20') } }),
      db.project.create({ data: { customerId: customers[4].id, name: 'Svenska E-handel — Webbutik', description: 'E-handelsplattform med produktkatalog', status: 'planning', startDate: new Date() } }),
      db.project.create({ data: { customerId: customers[2].id, name: 'Hälsokällan — Bokningssystem', description: 'Online-bokning och personalpresentation', status: 'review', startDate: new Date('2025-03-01') } }),
      db.project.create({ data: { customerId: customers[1].id, name: 'Nordbygg — Portfolio & offerter', description: 'Portfolio-sida med offerter-formulär', status: 'in_progress', startDate: new Date('2025-02-10') } }),
    ]);

    // Seed demo invoices
    await Promise.all([
      db.invoice.create({ data: { customerId: customers[0].id, amount: 9980, description: 'Upprättande Trattoria Bella — Pro-paket', status: 'paid', dueDate: new Date('2025-01-31'), paidDate: new Date('2025-01-28') } }),
      db.invoice.create({ data: { customerId: customers[1].id, amount: 14990, description: 'Upprättande Nordbygg AB — Premium-paket', status: 'pending', dueDate: new Date('2025-04-15') } }),
      db.invoice.create({ data: { customerId: customers[0].id, amount: 3990, description: 'Månadsavgift januari — Pro-paket', status: 'paid', dueDate: new Date('2025-01-31'), paidDate: new Date('2025-02-01') } }),
      db.invoice.create({ data: { customerId: customers[0].id, amount: 3990, description: 'Månadsavgift februari — Pro-paket', status: 'overdue', dueDate: new Date('2025-02-28') } }),
    ]);

    // Seed demo messages
    await Promise.all([
      db.contactMessage.create({ data: { name: 'Karl Pettersson', email: 'karl@petterssonsbygg.se', phone: '070-123 45 67', company: 'Petterssons Bygg', message: 'Hej! Vi söker en partner som kan bygga och driva vår hemsida. Vi är ett byggföretag med 15 anställda och behöver en snygg portfolio-sida.', read: false } }),
      db.contactMessage.create({ data: { name: 'Maria Eriksson', email: 'maria@blomstermåla.se', phone: '070-987 65 43', company: 'Blomstermåla Floristen', message: 'Vi driver en blomsterbutik och vill ha en hemsida med webbutik. Kan ni hjälpa oss? Vi behöver också e-post med vår domän.', read: false } }),
    ]);

    return NextResponse.json({ success: true, user: { id: user.id, email: user.email } });
  } catch (error) {
    console.error('Setup error:', error);
    return NextResponse.json({ error: 'Kunde inte skapa admin' }, { status: 500 });
  }
}
