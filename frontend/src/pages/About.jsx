import { useLanguage } from "../contexts/LanguageContext";
import { useTranslation } from "../translations";

export default function About() {
  const { language } = useLanguage();
  const t = useTranslation(language);

  return (
    <div className="bg-gray-800 rounded-lg shadow-xl p-6 space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-4">{t("aboutTitle")}</h2>
        <p className="text-gray-300">
          {t("aboutDescription")}
        </p>
      </div>

      {/* Languages Section */}
      <div>
        <h3 className="text-xl font-bold mb-3 text-red-400">{t("programmingLanguages")}</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-gray-700 rounded-lg p-4">
            <h4 className="font-semibold text-white mb-2">{t("backend")}</h4>
            <ul className="text-gray-300 space-y-1">
              <li>• <span className="font-medium">Python 3.11</span> — {language === "fr" ? "langage principal du backend" : "main backend language"}</li>
            </ul>
          </div>
          <div className="bg-gray-700 rounded-lg p-4">
            <h4 className="font-semibold text-white mb-2">{t("frontend")}</h4>
            <ul className="text-gray-300 space-y-1">
              <li>• <span className="font-medium">JavaScript (ES6+)</span> — {language === "fr" ? "langage principal du frontend" : "main frontend language"}</li>
              <li>• <span className="font-medium">JSX</span> — {language === "fr" ? "syntaxe React pour les composants" : "React component syntax"}</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Technologies Section */}
      <div>
        <h3 className="text-xl font-bold mb-3 text-red-400">{t("technologies")}</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-gray-700 rounded-lg p-4">
            <h4 className="font-semibold text-white mb-2">{t("backend")}</h4>
            <ul className="text-gray-300 space-y-1">
              <li>• <span className="font-medium">FastAPI</span> — framework web moderne et performant</li>
              <li>• <span className="font-medium">Uvicorn</span> — serveur ASGI pour FastAPI</li>
              <li>• <span className="font-medium">Redis</span> — cache en mémoire (optionnel)</li>
              <li>• <span className="font-medium">httpx</span> — client HTTP pour appeler l'API Ergast F1</li>
              <li>• <span className="font-medium">Pydantic</span> — validation de données</li>
            </ul>
          </div>
          <div className="bg-gray-700 rounded-lg p-4">
            <h4 className="font-semibold text-white mb-2">{t("frontend")}</h4>
            <ul className="text-gray-300 space-y-1">
              <li>• <span className="font-medium">React 18</span> — bibliothèque UI moderne</li>
              <li>• <span className="font-medium">Vite</span> — outil de build ultra-rapide</li>
              <li>• <span className="font-medium">React Router</span> — navigation entre pages</li>
              <li>• <span className="font-medium">Axios</span> — client HTTP pour l'API</li>
              <li>• <span className="font-medium">TailwindCSS</span> — framework CSS utility-first</li>
              <li>• <span className="font-medium">Nginx</span> — serveur web pour les fichiers statiques</li>
            </ul>
          </div>
        </div>
      </div>

      {/* DevOps Section */}
      <div>
        <h3 className="text-xl font-bold mb-3 text-red-400">{t("devopsInfra")}</h3>
        <div className="bg-gray-700 rounded-lg p-4">
          <ul className="text-gray-300 space-y-1">
            <li>• <span className="font-medium">Docker</span> — conteneurisation avec multi-stage builds</li>
            <li>• <span className="font-medium">Docker Compose</span> — orchestration locale des services</li>
            <li>• <span className="font-medium">GitHub Actions</span> — CI/CD (tests, lint, build, déploiement)</li>
            <li>• <span className="font-medium">Trivy</span> — scan de sécurité des images Docker</li>
            <li>• <span className="font-medium">GHCR</span> — GitHub Container Registry pour les images</li>
            <li>• <span className="font-medium">Railway</span> — hébergement des services en production</li>
          </ul>
        </div>
      </div>

      {/* Architecture Note */}
      <div className="bg-gray-900 border border-gray-700 rounded-lg p-4">
        <p className="text-gray-300 text-sm">
          <span className="font-semibold text-white">{t("architectureNote")}</span> {t("architectureText")} <code className="bg-gray-800 px-2 py-1 rounded text-red-300">{import.meta.env.VITE_API_URL || t("apiUrl")}</code>
        </p>
      </div>
    </div>
  );
}
