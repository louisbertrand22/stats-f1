import { useEffect, useState } from "react";
import { getDriverStandings, getHealth } from "../api";
import Loader from "../components/Loader";
import ErrorBanner from "../components/ErrorBanner";

export default function Home() {
  const [top3, setTop3] = useState([]);
  const [health, setHealth] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const [s, h] = await Promise.all([getDriverStandings(), getHealth()]);
        setTop3((s || []).slice(0, 3));
        setHealth(h);
      } catch (e) {
        setError(e?.message || "Erreur réseau");
      }
    })();
  }, []);

  if (!top3.length && !health && !error) return <Loader text="Chargement du dashboard..." />;

  return (
    <div>
      <ErrorBanner message={error} />

      <section className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
        <div className="px-6 py-4 bg-gray-700 flex items-center justify-between">
          <h2 className="text-2xl font-bold">Top 3 Pilotes</h2>
          {health && (
            <span className="text-sm text-gray-300">
              Mode: <b>{health.mode}</b> • Redis: {health.redis}
            </span>
          )}
        </div>
        <ul className="divide-y divide-gray-700">
          {top3.map((s) => (
            <li key={s.Driver?.driverId} className="px-6 py-4 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <span className="text-2xl">
                  {Number(s.position) === 1 ? "🥇" : Number(s.position) === 2 ? "🥈" : "🥉"}
                </span>
                <div>
                  <div className="font-semibold">
                    {s.Driver?.givenName} {s.Driver?.familyName}
                  </div>
                  <div className="text-sm text-gray-400">{s.Constructors?.[0]?.name}</div>
                </div>
              </div>
              <div className="text-red-400 font-bold text-xl">{s.points}</div>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
