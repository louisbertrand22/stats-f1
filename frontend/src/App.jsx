import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import LanguageSwitcher from "./components/LanguageSwitcher";
import Home from "./pages/Home";
import DriversStandings from "./pages/DriversStandings";
import ConstructorsStandings from "./pages/ConstructorsStandings";
import Schedule from "./pages/Schedule";
import About from "./pages/About";
import EasterEgg from "./pages/EasterEgg";
import PilotStats from "./pages/PilotStats";
import { LanguageProvider, useLanguage } from "./contexts/LanguageContext";
import { useTranslation } from "./translations";
import { API_URL } from "./api"; // <-- si tu as un api.js ; sinon supprime cette ligne

function AppContent() {
  const { language } = useLanguage();
  const t = useTranslation(language);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-white relative">
      {/* Background décoratif (grid + glow) */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 -z-10 
                   [mask-image:radial-gradient(ellipse_at_center,black_40%,transparent_70%)]"
      >
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,.035)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,.035)_1px,transparent_1px)] bg-[size:24px_24px]" />
        <div className="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[80vw] h-[40vh] rounded-full blur-3xl bg-red-600/20" />
      </div>

      {/* Header sticky + gradient + blur */}
      <header className="sticky top-0 z-40 backdrop-blur supports-[backdrop-filter]:bg-red-600/70 bg-red-600/90 shadow-[0_10px_30px_-10px_rgba(0,0,0,.5)]">
        <div className="container mx-auto px-4 py-4 flex flex-wrap items-center justify-between">
          <div>
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">
              <span className="mr-2">🏎️</span>{t("appTitle")}
            </h1>
            <p className="text-red-50/90 text-sm md:text-base mt-1">
              {t("appSubtitle")}
            </p>
          </div>

          {/* Badge d'environnement / URL API + Language Switcher */}
          <div className="flex items-center gap-2">
            <LanguageSwitcher />
            <span className="hidden sm:inline text-xs text-red-50/80">{t("apiLabel")}</span>
            <code className="text-[10px] sm:text-xs px-2 py-1 rounded-full bg-black/20 border border-white/10">
              {API_URL || t("apiUndefined")}
            </code>
          </div>
        </div>

        {/* Séparateur animé */}
        <div className="h-[3px] w-full bg-gradient-to-r from-transparent via-white/40 to-transparent animate-pulse" />
      </header>

      <BrowserRouter>
        <Navbar />

        {/* Shell “glass” pour le contenu */}
        <main className="container mx-auto px-4 py-8">
          <div className="rounded-2xl border border-white/10 bg-white/5 shadow-2xl backdrop-blur-sm">
            <div className="p-4 md:p-6">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/standings/drivers" element={<DriversStandings />} />
                <Route path="/standings/constructors" element={<ConstructorsStandings />} />
                <Route path="/stats/pilots" element={<PilotStats />} />
                <Route path="/schedule" element={<Schedule />} />
                <Route path="/about" element={<About />} />
                <Route path="/warp" element={<EasterEgg />} />
                <Route
                  path="*"
                  element={<div className="text-gray-300">{t("pageNotFound")}</div>}
                />
              </Routes>
            </div>
          </div>
        </main>

        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  );
}
