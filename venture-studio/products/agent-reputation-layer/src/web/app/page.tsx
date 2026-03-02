import Hero from './sections/Hero'
import Features from './sections/Features'
import Pricing from './sections/Pricing'
import Demo from './sections/Demo'
import CTA from './sections/CTA'

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950">
      <Hero />
      <Features />
      <Demo />
      <Pricing />
      <CTA />
    </main>
  )
}