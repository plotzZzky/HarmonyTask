import { Inter } from 'next/font/google'
import NavBar from '@elements/navbar'
import Footer from '@elements/footer'
import AppBar from '@elements/appBar'
import './page.css'


const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Buscar - HarmonyTask',
}

export default function RootLayout({ children }) {
  return (
    <section>
      <header>
        <NavBar></NavBar>
        <AppBar></AppBar>
      </header>

      <main>
        {children}
      </main>
      
      <Footer></Footer>
    </section>
  )
}
