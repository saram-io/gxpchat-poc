import './globals.css'
export const metadata = {
  title: 'GxPChat - ChatGPT for Life Sciences',
  description: 'Open source AI trained on FDA, EMA, ICH guidelines'
}
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-zinc-950 text-zinc-100">{children}</body>
    </html>
  )
}
