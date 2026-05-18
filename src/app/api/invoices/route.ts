import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET() {
  try {
    const invoices = await db.invoice.findMany({ orderBy: { createdAt: 'desc' }, include: { customer: { select: { companyName: true } } } });
    return NextResponse.json(invoices);
  } catch (error) {
    return NextResponse.json({ error: 'Kunde inte hämta fakturor' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const data = await request.json();
    const invoice = await db.invoice.create({ data });
    return NextResponse.json(invoice, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Kunde inte skapa faktura' }, { status: 500 });
  }
}
