import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET() {
  try {
    const projects = await db.project.findMany({ orderBy: { createdAt: 'desc' }, include: { customer: { select: { companyName: true } } } });
    return NextResponse.json(projects);
  } catch (error) {
    return NextResponse.json({ error: 'Kunde inte hämta projekt' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const data = await request.json();
    const project = await db.project.create({ data });
    return NextResponse.json(project, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Kunde inte skapa projekt' }, { status: 500 });
  }
}
