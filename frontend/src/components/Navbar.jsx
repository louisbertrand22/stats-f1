import { NavLink } from "react-router-dom";
import { useLanguage } from "../contexts/LanguageContext";
import { useTranslation } from "../translations";

const base =
  "px-4 py-2 rounded-lg font-semibold transition";
const active = "bg-red-600 text-white";
const idle = "bg-gray-800 text-gray-300 hover:bg-gray-700";

export default function Navbar() {
  const { language } = useLanguage();
  const t = useTranslation(language);
  const item = ({ isActive }) => (isActive ? `${base} ${active}` : `${base} ${idle}`);

  return (
    <nav className="container mx-auto px-4 py-4 flex flex-wrap gap-2">
      <NavLink to="/" className={item} end>{t("navHome")}</NavLink>
      <NavLink to="/standings/drivers" className={item}>{t("navDrivers")}</NavLink>
      <NavLink to="/standings/constructors" className={item}>{t("navConstructors")}</NavLink>
      <NavLink to="/stats/pilots" className={item}>{t("navStats")}</NavLink>
      <NavLink to="/schedule" className={item}>{t("navSchedule")}</NavLink>
      <NavLink to="/about" className={item}>{t("navAbout")}</NavLink>
      <NavLink to="/warp" className={item} title="👀">?</NavLink>
    </nav>
  );
}
