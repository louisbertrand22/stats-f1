import { useEffect, useState } from "react";
import { getSchedule, getRaceResult } from "../api";
import Loader from "../components/Loader";
import ErrorBanner from "../components/ErrorBanner";

export default function Schedule() {
  const [data, setData] = useState([]);
  const [raceResults, setRaceResults] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const schedule = await getSchedule();
        setData(schedule);
        
        // Fetch results for past races with controlled concurrency
        const today = new Date();
        const results = {};
        
        // Filter past races first
        const pastRaces = schedule.filter(race => new Date(race.date) < today);
        
        // Batch requests to avoid overwhelming the browser/server
        const BATCH_SIZE = 3; // Process 3 races at a time
        
        for (let i = 0; i < pastRaces.length; i += BATCH_SIZE) {
          const batch = pastRaces.slice(i, i + BATCH_SIZE);
          
          // Process batch concurrently
          const batchResults = await Promise.allSettled(
            batch.map(async (race) => {
              try {
                const result = await getRaceResult(race.season, race.round);
                if (result && result.Results) {
                  return {
                    key: `${race.season}-${race.round}`,
                    data: result.Results.slice(0, 3) // Get top 3
                  };
                }
              } catch (e) {
                // Results not available for this race, skip silently
              }
              return null;
            })
          );
          
          // Store successful results
          batchResults.forEach(({ status, value }) => {
            if (status === 'fulfilled' && value) {
              results[value.key] = value.data;
            }
          });
          
          // Small delay between batches to prevent overwhelming the server
          if (i + BATCH_SIZE < pastRaces.length) {
            await new Promise(resolve => setTimeout(resolve, 100));
          }
        }
        
        setRaceResults(results);
      } catch (e) { setError(e?.message || "Erreur"); }
    })();
  }, []);

  if (!data.length && !error) return <Loader text="Chargement du calendrier..." />;

  const isPastRace = (raceDate) => {
    const today = new Date();
    return new Date(raceDate) < today;
  };

  return (
    <div className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
      <div className="px-6 py-4 bg-gray-700">
        <h2 className="text-2xl font-bold">Calendrier de la saison</h2>
      </div>
      <ErrorBanner message={error} />
      <ul className="divide-y divide-gray-700">
        {data.map((r) => {
          const past = isPastRace(r.date);
          const podium = raceResults[`${r.season}-${r.round}`];
          
          return (
            <li key={`${r.season}-${r.round}`} className="px-6 py-4">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="font-semibold">
                    R{r.round} • {r.raceName}
                  </div>
                  <div className="text-sm text-gray-400">
                    {r.Circuit?.circuitName} — {r.Circuit?.Location?.locality}, {r.Circuit?.Location?.country}
                  </div>
                </div>
                <div className="text-gray-300">{r.date} {r.time?.replace("Z"," UTC")}</div>
              </div>
              
              {past && podium && (
                <div className="mt-3 pt-3 border-t border-gray-700">
                  <div className="text-sm font-semibold text-gray-300 mb-2">Podium</div>
                  <div className="flex gap-4">
                    {podium.map((result, index) => {
                      const medal = index === 0 ? "🥇" : index === 1 ? "🥈" : "🥉";
                      return (
                        <div key={result.position} className="flex items-center gap-2">
                          <span className="text-xl">{medal}</span>
                          <div className="text-sm">
                            <div className="text-gray-200">
                              {result.Driver?.givenName} {result.Driver?.familyName}
                            </div>
                            <div className="text-gray-400 text-xs">
                              {result.Constructor?.name}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
