import { NavLink } from "react-router-dom";

const base =
  "px-4 py-2 rounded-lg font-semibold transition";
const active = "bg-red-600 text-white";
const idle = "bg-gray-800 text-gray-300 hover:bg-gray-700";

export default function Navbar() {
  const item = ({ isActive }) => (isActive ? `${base} ${active}` : `${base} ${idle}`);

  return (
    <nav className="container mx-auto px-4 py-4 flex flex-wrap gap-2">
      <NavLink to="/" className={item} end>Accueil</NavLink>
      <NavLink to="/standings/drivers" className={item}>Pilotes</NavLink>
      <NavLink to="/standings/constructors" className={item}>Constructeurs</NavLink>
      <NavLink to="/schedule" className={item}>Calendrier</NavLink>
      <NavLink to="/about" className={item}>À propos</NavLink>
      <NavLink to="/warp" className={item} title="👀">?</NavLink>
    </nav>
  );
}
