import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "WebPro — Professionella hemsidor för svenska företag",
  description: "Vi skapar vackra, snabba och säkra hemsidor för företag i hela Sverige. WordPress, .SE-domän, e-post och hosting — allt i ett paket.",
  keywords: ["företag hemsida", "webbyrå Sverige", "WordPress företag", ".SE domän", "företags webbdesign Sverige"],
  authors: [{ name: "WebPro" }],
  openGraph: {
    title: "WebPro — Professionella hemsidor för svenska företag",
    description: "Vi skapar vackra, snabba och säkra hemsidor för företag i hela Sverige.",
    type: "website",
    siteName: "WebPro",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="sv" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        {children}
      </body>
    </html>
  );
}
