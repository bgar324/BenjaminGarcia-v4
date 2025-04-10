import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/next";
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
  title: "Benjamin Garcia",
  description: "Personal portfolio of Benjamin Garcia",
  icons: {
    icon: "/static/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" style={{ scrollBehavior: "smooth" }}>
      <head>
        <link
          rel="stylesheet"
          href="/fonts/CabinetGrotesk_Complete/Fonts/WEB/css/cabinet-grotesk.css"
        />
        <link
          rel="preload"
          as="image"
          href="/static/project-previews/csclubwebsite-preview.webp"
        />
        <link
          rel="preload"
          as="image"
          href="/static/project-previews/logit-preview.webp"
        />
        <link
          rel="preload"
          as="image"
          href="/static/project-previews/teaspots.webp"
        />
        <link
          rel="preload"
          as="image"
          href="/static/project-previews/suika-preview.webp"
        />
        <link
          rel="preload"
          as="image"
          href="/static/project-previews/portfoliov5.webp"
        />
        <link
          rel="preload"
          as="image"
          href="/static/project-previews/caduceus.webp"
        />
        <link
          rel="preload"
          as="image"
          href="/static/project-previews/image.webp"
        />
        <link
          rel="preload"
          as="image"
          href="/static/project-previews/weather-preview.webp"
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Analytics />
        <SpeedInsights />
        {children}
      </body>
    </html>
  );
}
