import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI-Powered Market Reaction Simulator",
  description: "Financial event simulation dashboard",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
