import { useEffect, useState } from "react";

const KONAMI = ["ArrowUp","ArrowUp","ArrowDown","ArrowDown","ArrowLeft","ArrowRight","ArrowLeft","ArrowRight","m","a", "x"];
export default function EasterEgg() {
  const [ok, setOk] = useState(false);

  useEffect(() => {
    let idx = 0;
    const onKey = (e) => {
      if (e.key === KONAMI[idx]) {
        idx++;
        if (idx === KONAMI.length) { setOk(true); idx = 0; }
      } else {
        idx = 0;
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <div className="bg-gray-800 rounded-lg shadow-xl p-6 text-center">
      <h2 className="text-2xl font-bold mb-2">Easter Egg</h2>
      <p className="text-gray-300 mb-6">Tape le <b>Max Code</b> sur ton clavier 🎮</p>

      <div className={`mx-auto w-48 h-48 rounded-full flex items-center justify-center text-5xl transition-all
        ${ok ? "bg-gradient-to-br from-red-500 to-yellow-400 animate-bounce" : "bg-gray-700"}`}>
        {ok ? "🏁" : "❓"}
      </div>

      {ok && <p className="mt-6 text-red-300">Boost activé ! Vroum vroum 🏎️💨</p>}
    </div>
  );
}
