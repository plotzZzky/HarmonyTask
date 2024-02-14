import { Inter } from 'next/font/google'
import '@/app/globals.css'
import Footer from '@comps/footer'
import NavBar from '@comps/navbar'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Início - HarmonyTask',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
        <body className={inter.className}>
          <header>
            <NavBar></NavBar>
          </header>

          {children}

          <Footer></Footer>
        </body>
    </html>
  )
}
