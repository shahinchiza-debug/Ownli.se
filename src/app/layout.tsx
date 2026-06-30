import type { Metadata, Viewport } from "next";
import { Sora, DM_Sans } from "next/font/google";
import "./globals.css";
import SmoothScroll from "@/components/shared/SmoothScroll";
import PageTransition from "@/components/shared/PageTransition";

const sora = Sora({
  variable: "--font-display",
  subsets: ["latin"],
  weight: ["400", "600", "700", "800"],
  display: "swap",
});

const dmSans = DM_Sans({
  variable: "--font-body",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Ownli — Professionella hemsidor för svenska företag",
  description: "Vi skapar vackra, snabba och säkra hemsidor för företag i hela Sverige. WordPress, .SE-domän, e-post och hosting — du äger, vi bygger.",
  keywords: ["företag hemsida", "webbyrå Sverige", "WordPress företag", ".SE domän", "företags webbdesign Sverige", "Ownli"],
  authors: [{ name: "Ownli" }],
  openGraph: {
    title: "Ownli — Professionella hemsidor för svenska företag",
    description: "Vi skapar vackra, snabba och säkra hemsidor för företag i hela Sverige. Du äger. Vi bygger.",
    type: "website",
    siteName: "Ownli",
    locale: "sv_SE",
  },
  icons: {
    icon: [
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
    ],
    apple: "/apple-touch-icon.png",
  },
};

export const viewport: Viewport = {
  themeColor: "#2563eb",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="sv" suppressHydrationWarning>
      <body
        className={`${sora.variable} ${dmSans.variable} antialiased bg-background text-foreground`}
      >
        <a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded-lg focus:text-sm focus:font-semibold">
          Hoppa till huvudinnehåll
        </a>
        <SmoothScroll>
          <PageTransition>
            {children}
          </PageTransition>
        </SmoothScroll>
      </body>
    </html>
  );
}
