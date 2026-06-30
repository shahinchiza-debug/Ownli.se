import Link from 'next/link';
import OwnliLogo from '@/components/OwnliLogo';

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-stone-950 text-white px-4">
      <div className="text-center max-w-lg">
        <div className="mb-8 flex justify-center">
          <OwnliLogo size={64} markOnly />
        </div>
        <h1 className="text-8xl sm:text-9xl font-bold font-[family-name:var(--font-display)] bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent mb-4">
          404
        </h1>
        <p className="text-xl sm:text-2xl text-stone-300 mb-2 font-[family-name:var(--font-display)]">Sidan hittades inte</p>
        <p className="text-stone-500 mb-10 leading-relaxed">
          Sidan du letar efter finns inte eller har flyttats. Låt oss hjälpa dig tillbaka på rätt spår.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/"
            className="inline-flex items-center justify-center h-12 px-8 rounded-full bg-blue-600 hover:bg-blue-700 text-white font-medium transition-colors shadow-lg shadow-blue-600/25"
          >
            Till startsidan
          </Link>
          <Link
            href="/kontakt"
            className="inline-flex items-center justify-center h-12 px-8 rounded-full border border-white/30 text-white hover:bg-white/10 font-medium transition-colors"
          >
            Kontakta oss
          </Link>
        </div>
      </div>
    </div>
  );
}
