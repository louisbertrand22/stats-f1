import { useLanguage } from "../contexts/LanguageContext";

export default function LanguageSwitcher() {
  const { language, toggleLanguage } = useLanguage();

  return (
    <button
      onClick={toggleLanguage}
      className="px-3 py-2 rounded-lg bg-black/20 border border-white/10 hover:bg-black/30 transition-colors flex items-center gap-2"
      title={language === "fr" ? "Switch to English" : "Passer en français"}
    >
      <span className="text-sm font-semibold">
        {language === "fr" ? "🇫🇷 FR" : "🇬🇧 EN"}
      </span>
    </button>
  );
}
