import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "")

function App() {
  const [drivers, setDrivers] = useState([])
  const [standings, setStandings] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('standings')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [standingsRes, driversRes] = await Promise.all([
        axios.get(`${API_URL}/standings/drivers`),
        axios.get(`${API_URL}/drivers/current`)
      ])
      setStandings(standingsRes.data)
      setDrivers(driversRes.data)
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-2xl">Chargement des données F1... 🏎️</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-red-600 shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-4xl font-bold">🏎️ F1 Dashboard</h1>
          <p className="text-red-100 mt-2">Statistiques en temps réel de la Formule 1</p>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex space-x-4 mb-8">
          <button
            onClick={() => setActiveTab('standings')}
            className={`px-6 py-3 rounded-lg font-semibold transition ${
              activeTab === 'standings'
                ? 'bg-red-600 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            Classement
          </button>
          <button
            onClick={() => setActiveTab('drivers')}
            className={`px-6 py-3 rounded-lg font-semibold transition ${
              activeTab === 'drivers'
                ? 'bg-red-600 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            Pilotes
          </button>
        </div>

        {/* Classement */}
        {activeTab === 'standings' && (
          <div className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
            <div className="px-6 py-4 bg-gray-700">
              <h2 className="text-2xl font-bold">Classement des Pilotes</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left">Position</th>
                    <th className="px-6 py-3 text-left">Pilote</th>
                    <th className="px-6 py-3 text-left">Ecurie</th>
                    <th className="px-6 py-3 text-left">Points</th>
                    <th className="px-6 py-3 text-left">Victoires</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {standings.map((standing) => (
                    <tr
                      key={standing.position}
                      className="hover:bg-gray-700 transition"
                    >
                      <td className="px-6 py-4 font-bold text-xl">
                        {standing.position === '1' && '🥇'}
                        {standing.position === '2' && '🥈'}
                        {standing.position === '3' && '🥉'}
                        {standing.position > 3 && standing.position}
                      </td>
                      <td className="px-6 py-4">
                        <div>
                          <div className="font-semibold">
                            {standing.Driver.givenName} {standing.Driver.familyName}
                          </div>
                          <div className="text-sm text-gray-400">
                            {standing.Driver.nationality}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        {standing.Constructors[0].name}
                      </td>
                      <td className="px-6 py-4 font-bold text-red-400">
                        {standing.points}
                      </td>
                      <td className="px-6 py-4">{standing.wins}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Liste des pilotes */}
        {activeTab === 'drivers' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {drivers.map((driver) => (
              <div
                key={driver.driverId}
                className="bg-gray-800 rounded-lg shadow-xl p-6 hover:bg-gray-700 transition"
              >
                <div className="flex items-center space-x-4">
                  <div className="text-4xl">🏁</div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold">
                      {driver.givenName} {driver.familyName}
                    </h3>
                    <p className="text-gray-400">{driver.nationality}</p>
                    <p className="text-sm text-gray-500">
                      #{driver.permanentNumber || 'N/A'}
                    </p>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-gray-700">
                  <p className="text-sm text-gray-400">
                    Date de naissance: {driver.dateOfBirth}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <footer className="bg-gray-800 mt-12 py-6">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p>Données fournies par l'API Ergast F1</p>
          <p className="text-sm mt-2">Projet DevOps - Apprentissage</p>
        </div>
      </footer>
    </div>
  )
}

export default App