import { useEffect, useState } from "react";
import { getDriverStandings, getHealth, getRaceResult, getSchedule } from "../api";
import Loader from "../components/Loader";
import ErrorBanner from "../components/ErrorBanner";

export default function Home() {
  const [top3, setTop3] = useState([]);
  const [health, setHealth] = useState(null);
  const [lastRace, setLastRace] = useState(null);
  const [nextRace, setNextRace] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const [s, h, schedule] = await Promise.all([
          getDriverStandings(), 
          getHealth(), 
          getSchedule()
        ]);
        setTop3((s || []).slice(0, 3));
        setHealth(h);
        
        // Find last and next races from schedule
        if (schedule && schedule.length > 0) {
          const today = new Date();
          
          // Find the last completed race (most recent race before today)
          const pastRaces = schedule.filter(race => new Date(race.date) < today);
          if (pastRaces.length > 0) {
            const lastCompletedRace = pastRaces[pastRaces.length - 1];
            try {
              const result = await getRaceResult(lastCompletedRace.season, lastCompletedRace.round);
              if (result && result.Results) {
                setLastRace(result);
              }
            } catch (e) {
              // Results not available for this race
            }
          }
          
          // Find next race (first race after today)
          const upcoming = schedule.find(race => new Date(race.date) > today);
          setNextRace(upcoming || null);
        }
      } catch (e) {
        setError(e?.message || "Erreur réseau");
      }
    })();
  }, []);

  if (!top3.length && !health && !error) return <Loader text="Chargement du dashboard..." />;

  return (
    <div className="space-y-6">
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

      {lastRace && lastRace.Results && (
        <section className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
          <div className="px-6 py-4 bg-gray-700">
            <h2 className="text-2xl font-bold">Dernière Course</h2>
          </div>
          <div className="px-6 py-4">
            <div className="mb-3">
              <div className="font-semibold text-lg">
                {lastRace.raceName}
              </div>
              <div className="text-sm text-gray-400">
                {lastRace.Circuit?.circuitName} — {lastRace.Circuit?.Location?.locality}, {lastRace.Circuit?.Location?.country}
              </div>
              <div className="text-sm text-gray-400">
                {lastRace.date} {lastRace.time?.replace("Z", " UTC")}
              </div>
            </div>
            <div className="border-t border-gray-700 pt-3">
              <div className="text-sm font-semibold text-gray-300 mb-2">Podium</div>
              <div className="flex flex-col gap-3">
                {lastRace.Results.slice(0, 3).map((result, index) => {
                  const medal = index === 0 ? "🥇" : index === 1 ? "🥈" : "🥉";
                  return (
                    <div key={result.position} className="flex items-center gap-3">
                      <span className="text-2xl">{medal}</span>
                      <div className="flex-1">
                        <div className="font-semibold text-gray-200">
                          {result.Driver?.givenName} {result.Driver?.familyName}
                        </div>
                        <div className="text-sm text-gray-400">
                          {result.Constructor?.name}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </section>
      )}

      {nextRace && (
        <section className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
          <div className="px-6 py-4 bg-gray-700">
            <h2 className="text-2xl font-bold">Prochaine Course</h2>
          </div>
          <div className="px-6 py-4">
            <div className="font-semibold text-lg mb-2">
              Round {nextRace.round} • {nextRace.raceName}
            </div>
            <div className="text-sm text-gray-400">
              {nextRace.Circuit?.circuitName}
            </div>
            <div className="text-sm text-gray-400 mb-1">
              {nextRace.Circuit?.Location?.locality}, {nextRace.Circuit?.Location?.country}
            </div>
            <div className="text-gray-300 font-semibold mt-3">
              📅 {nextRace.date} {nextRace.time?.replace("Z", " UTC")}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
