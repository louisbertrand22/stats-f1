import { useLanguage } from "../contexts/LanguageContext";
import { useTranslation } from "../translations";

export default function Footer() {
  const { language } = useLanguage();
  const t = useTranslation(language);
  
  return (
    <footer className="bg-gray-800 mt-12 py-6">
      <div className="container mx-auto px-4 text-center text-gray-400">
        <p>{t("footerDataProvided")} • {t("footerFrontCalls")} {import.meta.env.VITE_API_URL || t("footerNotDefined")}</p>
        <p className="text-sm mt-2">{t("footerProjectDescription")}</p>
        <p><a href="https://github.com/louisbertrand22/stats-f1" className="text-gray-400 hover:text-white">{t("footerGitHub")}</a></p>
        <p>{t("footerCopyright")}</p>
      </div>
    </footer>
  );
}
