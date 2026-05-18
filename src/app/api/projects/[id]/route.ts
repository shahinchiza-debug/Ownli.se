import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function PUT(request: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const data = await request.json();
    const project = await db.project.update({ where: { id }, data });
    return NextResponse.json(project);
  } catch (error) {
    return NextResponse.json({ error: 'Kunde inte uppdatera projekt' }, { status: 500 });
  }
}

export async function DELETE(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    await db.project.delete({ where: { id } });
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Kunde inte radera projekt' }, { status: 500 });
  }
}
