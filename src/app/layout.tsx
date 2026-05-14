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
  title: "RestWeb — Professionella hemsidor för svenska restauranger",
  description: "Vi skapar vackra, snabba och säkra hemsidor för restauranger i hela Sverige. WordPress, .SE-domän, e-post och hosting — allt i ett paket.",
  keywords: ["restaurang hemsida", "webbyrå restaurang", "WordPress restaurang", ".SE domän", "restaurang webbdesign Sverige"],
  authors: [{ name: "RestWeb" }],
  openGraph: {
    title: "RestWeb — Professionella hemsidor för svenska restauranger",
    description: "Vi skapar vackra, snabba och säkra hemsidor för restauranger i hela Sverige.",
    type: "website",
    siteName: "RestWeb",
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
