import { Inter } from 'next/font/google'
import '@/app/globals.css'
import { AuthProvider } from '@comps/authContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Início - HarmonyTask',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
        <AuthProvider>
          <body className={inter.className}>
            {children}
          </body>
        </AuthProvider>  
    </html>
  )
}
