export default function About() {
  return (
    <div className="bg-gray-800 rounded-lg shadow-xl p-6">
      <h2 className="text-2xl font-bold mb-4">À propos</h2>
      <p className="text-gray-300">
        F1 Dashboard est un projet d'apprentissage DevOps : FastAPI (backend), React+Vite (frontend), Docker, CI/CD GitHub Actions,
        scans Trivy, images publiées sur GHCR et déployées sur Railway.
      </p>
      <ul className="list-disc list-inside mt-4 text-gray-300 space-y-1">
        <li>Backend FastAPI — endpoints REST, cache Redis (optionnel)</li>
        <li>Frontend React — pages statiques servies par Nginx</li>
        <li>Pas de proxy /api : le front appelle {import.meta.env.VITE_API_URL || "l’URL de l’API"}</li>
      </ul>
    </div>
  );
}
