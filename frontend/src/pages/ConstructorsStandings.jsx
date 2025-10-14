import { useEffect, useState } from "react";
import { getConstructorStandings } from "../api";
import Loader from "../components/Loader";
import ErrorBanner from "../components/ErrorBanner";
import { useLanguage } from "../contexts/LanguageContext";
import { useTranslation } from "../translations";

export default function ConstructorsStandings() {
  const { language } = useLanguage();
  const t = useTranslation(language);
  const [data, setData] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setData(await getConstructorStandings());
      } catch (e) { setError(e?.message || t("error")); }
    })();
  }, [t]);

  if (!data.length && !error) return <Loader text={t("loadingConstructors")} />;

  return (
    <div className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
      <div className="px-6 py-4 bg-gray-700">
        <h2 className="text-2xl font-bold">{t("constructorsStandings")}</h2>
      </div>
      <ErrorBanner message={error} />
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left">{t("pos")}</th>
              <th className="px-6 py-3 text-left">{t("team")}</th>
              <th className="px-6 py-3 text-left">{t("points")}</th>
              <th className="px-6 py-3 text-left">{t("wins")}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {data.map((c) => (
              <tr key={`${c.position}-${c.Constructor?.constructorId}`} className="hover:bg-gray-700 transition">
                <td className="px-6 py-4 font-bold">{c.position}</td>
                <td className="px-6 py-4">{c.Constructor?.name}</td>
                <td className="px-6 py-4 font-bold text-red-400">{c.points}</td>
                <td className="px-6 py-4">{c.wins ?? "0"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
