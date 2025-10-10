import { useEffect, useState } from "react";
import { getSchedule } from "../api";
import Loader from "../components/Loader";
import ErrorBanner from "../components/ErrorBanner";

export default function Schedule() {
  const [data, setData] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setData(await getSchedule());
      } catch (e) { setError(e?.message || "Erreur"); }
    })();
  }, []);

  if (!data.length && !error) return <Loader text="Chargement du calendrier..." />;

  return (
    <div className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
      <div className="px-6 py-4 bg-gray-700">
        <h2 className="text-2xl font-bold">Calendrier de la saison</h2>
      </div>
      <ErrorBanner message={error} />
      <ul className="divide-y divide-gray-700">
        {data.map((r) => (
          <li key={`${r.season}-${r.round}`} className="px-6 py-4 flex items-center justify-between">
            <div>
              <div className="font-semibold">
                R{r.round} • {r.raceName}
              </div>
              <div className="text-sm text-gray-400">
                {r.Circuit?.circuitName} — {r.Circuit?.Location?.locality}, {r.Circuit?.Location?.country}
              </div>
            </div>
            <div className="text-gray-300">{r.date} {r.time?.replace("Z"," UTC")}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
