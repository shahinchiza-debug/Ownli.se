import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function PUT(request: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const data = await request.json();
    const message = await db.contactMessage.update({ where: { id }, data });
    return NextResponse.json(message);
  } catch (error) {
    return NextResponse.json({ error: 'Kunde inte uppdatera meddelande' }, { status: 500 });
  }
}

export async function DELETE(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    await db.contactMessage.delete({ where: { id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Kunde inte radera meddelande' }, { status: 500 });
  }
}
