export default function Footer() {
  return (
    <footer className="bg-gray-800 mt-12 py-6">
      <div className="container mx-auto px-4 text-center text-gray-400">
        <p>Données fournies par l'API Ergast F1 • Front appelle {import.meta.env.VITE_API_URL || "N/D"}</p>
        <p className="text-sm mt-2">Projet DevOps - Apprentissage</p>
        <p><a href="https://github.com/louisbertrand22/stats-f1" className="text-gray-400 hover:text-white">GitHub</a></p>
        <p>copyright 2025 - Tous droits réservés - Louis BERTRAND</p>
      </div>
    </footer>
  );
}
