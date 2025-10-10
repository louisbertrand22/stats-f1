import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')

// Axios instance
const api = axios.create({
  baseURL: API_URL,
  timeout: 15000,
  headers: { 'X-Requested-With': 'XMLHttpRequest' }
})

function App() {
  const [drivers, setDrivers] = useState([])
  const [standings, setStandings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('standings')

  useEffect(() => {
    loadData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      setError('')
      const [standingsRes, driversRes] = await Promise.all([
        api.get('/standings/drivers'),
        api.get('/drivers/current'),
      ])
      const sRaw = standingsRes?.data;
      const dRaw = driversRes?.data;

      // si jamais ton backend renvoyait une autre forme (par ex. objet),
      // on force en tableau pour éviter ".map is not a function"
      const s = Array.isArray(sRaw)
        ? sRaw
        : (sRaw?.MRData?.StandingsTable?.StandingsLists?.[0]?.DriverStandings ?? []);
      const d = Array.isArray(dRaw) ? dRaw : toArray(dRaw);
      console.log('API_URL:', API_URL);
      console.log('standings raw type:', typeof sRaw, sRaw);
      console.log('drivers raw type:', typeof dRaw, dRaw);
      setStandings(standingsRes.data || [])
      setDrivers(driversRes.data || [])
    } catch (err) {
      console.error('Erreur lors du chargement des données:', err)
      const msg = err?.response?.data?.detail || err.message || 'Erreur réseau'
      setError(`Impossible de charger les données (${msg}).`)
    } finally {
      setLoading(false)
    }
  }

  const Banner = () =>
    (!API_URL) ? (
      <div className="bg-yellow-600 text-black px-4 py-2 text-sm text-center">
        ⚠️ VITE_API_URL est vide. Configure l’URL de l’API au build.
      </div>
    ) : null

  const SkeletonRow = ({ count = 10 }) => (
    <tbody className="divide-y divide-gray-700">
      {Array.from({ length: count }).map((_, i) => (
        <tr key={`sk-${i}`} className="animate-pulse">
          <td className="px-6 py-4"><div className="h-4 bg-gray-700 rounded w-10" /></td>
          <td className="px-6 py-4"><div className="h-4 bg-gray-700 rounded w-40 mb-2" /><div className="h-3 bg-gray-800 rounded w-24" /></td>
          <td className="px-6 py-4"><div className="h-4 bg-gray-700 rounded w-32" /></td>
          <td className="px-6 py-4"><div className="h-4 bg-gray-700 rounded w-12" /></td>
          <td className="px-6 py-4"><div className="h-4 bg-gray-700 rounded w-12" /></td>
        </tr>
      ))}
    </tbody>
  )

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Banner />

      <header className="bg-red-600 shadow-lg">
        <div className="container mx-auto px-4 py-6 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold">🏎️ F1 Dashboard</h1>
            <p className="text-red-100 mt-2">Statistiques en temps réel de la Formule 1</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-red-100 opacity-80">API:</span>
            <code className="text-xs bg-red-700/40 px-2 py-1 rounded">{API_URL || 'NON DÉFINIE'}</code>
            <button
              onClick={loadData}
              className="ml-3 px-3 py-2 bg-black/20 hover:bg-black/30 rounded border border-white/20 text-sm"
              title="Rafraîchir"
            >
              ↻ Refresh
            </button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6">
        {error && (
          <div className="bg-red-600/20 border border-red-600/40 text-red-200 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Tabs */}
        <div className="flex space-x-4 mb-6">
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
        {activeTab === 'standings' && Array.isArray(standings) && (
          <div className="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
            <div className="px-6 py-4 bg-gray-700 flex items-center justify-between">
              <h2 className="text-2xl font-bold">Classement des Pilotes</h2>
              <span className="text-gray-300 text-sm">
                {loading ? 'Chargement…' : `${standings.length} entrées`}
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left">Position</th>
                    <th className="px-6 py-3 text-left">Pilote</th>
                    <th className="px-6 py-3 text-left">Écurie</th>
                    <th className="px-6 py-3 text-left">Points</th>
                    <th className="px-6 py-3 text-left">Victoires</th>
                  </tr>
                </thead>

                {loading ? (
                  <SkeletonRow count={10} />
                ) : (
                  <tbody className="divide-y divide-gray-700">
                    {standings.map((s) => {
                      const pos = Number(s.position)
                      return (
                        <tr key={`${pos}-${s.Driver?.driverId || s.Driver?.code}`} className="hover:bg-gray-700 transition">
                          <td className="px-6 py-4 font-bold text-xl">
                            {pos === 1 ? '🥇' : pos === 2 ? '🥈' : pos === 3 ? '🥉' : pos}
                          </td>
                          <td className="px-6 py-4">
                            <div>
                              <div className="font-semibold">
                                {s.Driver?.givenName} {s.Driver?.familyName}
                              </div>
                              <div className="text-sm text-gray-400">
                                {s.Driver?.nationality}
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            {s.Constructors?.[0]?.name || '—'}
                          </td>
                          <td className="px-6 py-4 font-bold text-red-400">
                            {s.points}
                          </td>
                          <td className="px-6 py-4">{s.wins ?? '0'}</td>
                        </tr>
                      )
                    })}
                  </tbody>
                )}
              </table>
            </div>
          </div>
        )}

        {/* Liste des pilotes */}
        {activeTab === 'drivers' && Array.isArray(drivers) && (
          <div>
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {Array.from({ length: 9 }).map((_, i) => (
                  <div key={`skd-${i}`} className="bg-gray-800 rounded-lg shadow-xl p-6 animate-pulse">
                    <div className="h-6 bg-gray-700 rounded w-48 mb-3"></div>
                    <div className="h-4 bg-gray-700 rounded w-24 mb-2"></div>
                    <div className="h-4 bg-gray-700 rounded w-16"></div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {drivers.map((d) => (
                  <div key={d.driverId} className="bg-gray-800 rounded-lg shadow-xl p-6 hover:bg-gray-700 transition">
                    <div className="flex items-center space-x-4">
                      <div className="text-4xl">🏁</div>
                      <div className="flex-1">
                        <h3 className="text-xl font-bold">
                          {d.givenName} {d.familyName}
                        </h3>
                        <p className="text-gray-400">{d.nationality}</p>
                        <p className="text-sm text-gray-500">#{d.permanentNumber || 'N/A'}</p>
                      </div>
                    </div>
                    <div className="mt-4 pt-4 border-t border-gray-700 text-sm text-gray-300">
                      Date de naissance : {d.dateOfBirth}
                    </div>
                  </div>
                ))}
              </div>
            )}
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
