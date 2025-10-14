import { useEffect, useState } from "react";
import { getDriverStandings } from "../api";
import Loader from "../components/Loader";
import ErrorBanner from "../components/ErrorBanner";
import { useLanguage } from "../contexts/LanguageContext";
import { useTranslation } from "../translations";

export default function DriversStandings() {
  const { language } = useLanguage();
  const t = useTranslation(language);
  const [data, setData] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setData(await getDriverStandings());
      } catch (e) { setError(e?.message || t("error")); }
    })();
  }, [t]);

  if (!data.length && !error) return <Loader text={t("loadingDrivers")} />;

  return (
    <div className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
      <div className="px-6 py-4 bg-gray-700">
        <h2 className="text-2xl font-bold">{t("driversStandings")}</h2>
      </div>
      <ErrorBanner message={error} />
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left">{t("pos")}</th>
              <th className="px-6 py-3 text-left">{t("driver")}</th>
              <th className="px-6 py-3 text-left">{t("constructor")}</th>
              <th className="px-6 py-3 text-left">{t("points")}</th>
              <th className="px-6 py-3 text-left">{t("wins")}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {data.map((s) => (
              <tr key={`${s.position}-${s.Driver?.driverId}`} className="hover:bg-gray-700 transition">
                <td className="px-6 py-4 font-bold">{s.position}</td>
                <td className="px-6 py-4">
                  <div className="font-semibold">
                    {s.Driver?.givenName} {s.Driver?.familyName}
                  </div>
                  <div className="text-sm text-gray-400">{s.Driver?.nationality}</div>
                </td>
                <td className="px-6 py-4">{s.Constructors?.[0]?.name}</td>
                <td className="px-6 py-4 font-bold text-red-400">{s.points}</td>
                <td className="px-6 py-4">{s.wins ?? "0"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
