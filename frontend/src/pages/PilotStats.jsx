import { useEffect, useState } from "react";
import { getAllDriverStats } from "../api";
import Loader from "../components/Loader";
import ErrorBanner from "../components/ErrorBanner";
import { useLanguage } from "../contexts/LanguageContext";
import { useTranslation } from "../translations";

export default function PilotStats() {
  const { language } = useLanguage();
  const t = useTranslation(language);
  const [data, setData] = useState([]);
  const [error, setError] = useState("");
  const [sortBy, setSortBy] = useState("wins");
  const [filterMin, setFilterMin] = useState(0);

  useEffect(() => {
    (async () => {
      try {
        setData(await getAllDriverStats());
      } catch (e) {
        setError(e?.message || t("error"));
      }
    })();
  }, [t]);

  if (!data.length && !error) return <Loader text={t("loadingStats")} />;

  // Sort data based on selected filter
  const getSortedData = () => {
    let filtered = [...data];
    
    // Filter based on minimum value
    if (filterMin > 0) {
      switch (sortBy) {
        case "wins":
          filtered = filtered.filter(d => d.total_wins >= filterMin);
          break;
        case "poles":
          filtered = filtered.filter(d => d.total_poles >= filterMin);
          break;
        case "podiums":
          filtered = filtered.filter(d => d.total_podiums >= filterMin);
          break;
        case "races":
          filtered = filtered.filter(d => d.total_races >= filterMin);
          break;
      }
    }

    // Sort
    return filtered.sort((a, b) => {
      switch (sortBy) {
        case "wins":
          return b.total_wins - a.total_wins;
        case "poles":
          return b.total_poles - a.total_poles;
        case "podiums":
          return b.total_podiums - a.total_podiums;
        case "races":
          return b.total_races - a.total_races;
        default:
          return 0;
      }
    });
  };

  const sortedData = getSortedData();

  return (
    <div className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
      <div className="px-6 py-4 bg-gray-700">
        <h2 className="text-2xl font-bold mb-4">{t("pilotStats")}</h2>
        
        {/* Filter controls */}
        <div className="flex flex-wrap gap-4 items-center">
          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-300">{t("sortBy")}</label>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 rounded bg-gray-600 text-white border border-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <option value="wins">{t("wins")}</option>
              <option value="poles">{t("poles")}</option>
              <option value="podiums">{t("podiums")}</option>
              <option value="races">{t("races")}</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-300">{t("minimum")}</label>
            <input
              type="number"
              min="0"
              value={filterMin}
              onChange={(e) => setFilterMin(parseInt(e.target.value) || 0)}
              className="w-20 px-3 py-2 rounded bg-gray-600 text-white border border-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500"
            />
          </div>

          {filterMin > 0 && (
            <button
              onClick={() => setFilterMin(0)}
              className="px-3 py-2 text-sm rounded bg-red-600 hover:bg-red-700 text-white transition"
            >
              {t("reset")}
            </button>
          )}
        </div>
      </div>

      <ErrorBanner message={error} />

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left">{t("driver")}</th>
              <th className="px-6 py-3 text-center cursor-pointer hover:bg-gray-600 transition"
                  onClick={() => setSortBy("wins")}>
                {t("wins")} {sortBy === "wins" && "⬇"}
              </th>
              <th className="px-6 py-3 text-center cursor-pointer hover:bg-gray-600 transition"
                  onClick={() => setSortBy("poles")}>
                {t("poles")} {sortBy === "poles" && "⬇"}
              </th>
              <th className="px-6 py-3 text-center cursor-pointer hover:bg-gray-600 transition"
                  onClick={() => setSortBy("podiums")}>
                {t("podiums")} {sortBy === "podiums" && "⬇"}
              </th>
              <th className="px-6 py-3 text-center cursor-pointer hover:bg-gray-600 transition"
                  onClick={() => setSortBy("races")}>
                {t("races")} {sortBy === "races" && "⬇"}
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {sortedData.map((driver) => (
              <tr key={driver.driver_id} className="hover:bg-gray-700 transition">
                <td className="px-6 py-4">
                  <div className="font-semibold">{driver.name}</div>
                  <div className="text-sm text-gray-400">{driver.driver_id}</div>
                </td>
                <td className="px-6 py-4 text-center font-bold text-red-400">
                  {driver.total_wins}
                </td>
                <td className="px-6 py-4 text-center font-bold text-yellow-400">
                  {driver.total_poles}
                </td>
                <td className="px-6 py-4 text-center font-bold text-blue-400">
                  {driver.total_podiums}
                </td>
                <td className="px-6 py-4 text-center text-gray-300">
                  {driver.total_races}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {sortedData.length === 0 && !error && (
          <div className="px-6 py-8 text-center text-gray-400">
            {t("noDrivers")}
          </div>
        )}
      </div>
    </div>
  );
}
