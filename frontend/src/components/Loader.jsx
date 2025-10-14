import { useLanguage } from "../contexts/LanguageContext";
import { useTranslation } from "../translations";

export default function Loader({ text }) {
  const { language } = useLanguage();
  const t = useTranslation(language);
  const displayText = text || t("defaultLoading");
  
  return (
    <div className="flex items-center justify-center py-10">
      <div className="animate-spin inline-block w-6 h-6 border-[3px] border-current border-t-transparent text-red-500 rounded-full mr-3" />
      <span className="text-gray-300">{displayText}</span>
    </div>
  );
}
