import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET() {
  try {
    const totalCustomers = await db.customer.count();
    const activeProjects = await db.project.count({ where: { status: { in: ['in_progress', 'review', 'planning'] } } });
    const unpaidInvoices = await db.invoice.count({ where: { status: { in: ['pending', 'overdue'] } } });
    const unreadMessages = await db.contactMessage.count({ where: { read: false } });

    const paidThisMonth = await db.invoice.findMany({
      where: { status: 'paid', paidDate: { gte: new Date(new Date().getFullYear(), new Date().getMonth(), 1) } },
    });
    const revenueThisMonth = paidThisMonth.reduce((sum, inv) => sum + inv.amount, 0);

    const recentCustomers = await db.customer.findMany({ orderBy: { createdAt: 'desc' }, take: 5 });
    const recentMessages = await db.contactMessage.findMany({ orderBy: { createdAt: 'desc' }, take: 5 });

    return NextResponse.json({
      totalCustomers, activeProjects, revenueThisMonth, unpaidInvoices, unreadMessages,
      recentCustomers, recentMessages,
    });
  } catch (error) {
    console.error('Stats error:', error);
    return NextResponse.json({ error: 'Kunde inte hämta statistik' }, { status: 500 });
  }
}
