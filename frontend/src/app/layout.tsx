import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DETOUR — 남는 시간을 나만의 우회로로",
  description: "현재 위치와 목적지 사이의 남는 시간에 맞는 작은 우회로를 추천합니다.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
