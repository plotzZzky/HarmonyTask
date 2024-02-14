import { Inter } from 'next/font/google'
import NavBar from '@comps/navbar'
import Footer from '@comps/footer'
import AppBar from '@comps/appBar'
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
