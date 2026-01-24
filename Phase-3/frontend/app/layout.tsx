import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
import Link from "next/link";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Todo App",
  description: "A simple and powerful todo application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
       <Providers>
          <nav className="bg-gray-800 text-white p-4">
            <div className="container mx-auto flex space-x-4">
              <Link href="/" className="hover:underline">Home</Link>
              <Link href="/tasks" className="hover:underline">Tasks</Link>
              <Link href="/chat" className="hover:underline">AI Assistant</Link>
              <Link href="/dashboard" className="hover:underline">Dashboard</Link>
            </div>
          </nav>

          <main className="container mx-auto p-4">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}