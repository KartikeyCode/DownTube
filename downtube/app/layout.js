import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'DownTube',
  description: 'Explore our free YouTube to MP3 and MP4 downloader – the ultimate online tool for converting your favorite YouTube videos to high-quality audio and video formats. Download music and videos effortlessly in just a few clicks. No software installation needed! Enjoy your favorite content offline on any device. Fast, secure, and easy to use.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
