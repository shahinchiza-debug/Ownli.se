import { NextResponse } from 'next/server';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';

export async function POST(request: Request) {
  try {
    const { email, password } = await request.json();
    if (!email || !password) {
      return NextResponse.json({ error: 'E-post och lösenord krävs' }, { status: 400 });
    }

    // Auto-setup if no users exist
    const userCount = await db.user.count();
    if (userCount === 0) {
      await fetch(new URL('/api/auth/setup', request.url), { method: 'POST' });
    }

    const user = await db.user.findUnique({ where: { email } });
    if (!user || !(await bcrypt.compare(password, user.password))) {
      return NextResponse.json({ error: 'Ogiltiga inloggningsuppgifter' }, { status: 401 });
    }

    const res = NextResponse.json({ success: true, user: { id: user.id, email: user.email, name: user.name, role: user.role } });
    res.cookies.set('ownli_session', user.id, { httpOnly: true, maxAge: 86400, path: '/' });
    return res;
  } catch (error) {
    console.error('Login error:', error);
    return NextResponse.json({ error: 'Inloggningsfel' }, { status: 500 });
  }
}
