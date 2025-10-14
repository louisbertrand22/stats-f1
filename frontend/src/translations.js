export const translations = {
  fr: {
    // Header
    appTitle: "F1 Dashboard",
    appSubtitle: "Statistiques en temps réel de la Formule 1",
    apiLabel: "API",
    apiUndefined: "non définie",
    
    // Navigation
    navHome: "Accueil",
    navDrivers: "Pilotes",
    navConstructors: "Constructeurs",
    navStats: "Statistiques",
    navSchedule: "Calendrier",
    navAbout: "À propos",
    
    // Home page
    top3Drivers: "Top 3 Pilotes",
    mode: "Mode",
    lastRace: "Dernière Course",
    nextRace: "Prochaine Course",
    podium: "Podium",
    loading: "Chargement du dashboard...",
    networkError: "Erreur réseau",
    pageNotFound: "Page introuvable.",
    
    // About page
    aboutTitle: "À propos du projet",
    aboutDescription: "F1 Dashboard est un projet d'apprentissage DevOps : FastAPI (backend), React+Vite (frontend), Docker, CI/CD GitHub Actions, scans Trivy, images publiées sur GHCR et déployées sur Railway.",
    programmingLanguages: "🗣️ Langages de programmation",
    backend: "Backend",
    frontend: "Frontend",
    technologies: "🧰 Technologies utilisées",
    devopsInfra: "🚀 DevOps & Infrastructure",
    architectureNote: "Note d'architecture :",
    architectureText: "Pas de proxy /api — le frontend appelle directement",
    apiUrl: "l'URL de l'API",
    
    // Driver Standings
    driversStandings: "Classement des Pilotes",
    position: "Position",
    driver: "Pilote",
    constructor: "Constructeur",
    points: "Points",
    wins: "Victoires",
    
    // Constructor Standings
    constructorsStandings: "Classement des Constructeurs",
    
    // Schedule
    schedule: "Calendrier",
    round: "Round",
    grandPrix: "Grand Prix",
    circuit: "Circuit",
    location: "Lieu",
    date: "Date",
    scheduleTitle: "Calendrier de la saison",
    loadingSchedule: "Chargement du calendrier...",
    
    // Pilot Stats
    pilotStats: "Statistiques des Pilotes",
    nationality: "Nationalité",
    permanentNumber: "Numéro permanent",
    code: "Code",
    sortBy: "Trier par:",
    minimum: "Minimum:",
    reset: "Réinitialiser",
    loadingStats: "Chargement des statistiques...",
    poles: "Pole Positions",
    podiums: "Podiums",
    races: "Courses",
    noDrivers: "Aucun pilote ne correspond aux critères de filtrage.",
    
    // Drivers/Constructors Standings
    loadingDrivers: "Classement pilotes...",
    loadingConstructors: "Classement constructeurs...",
    pos: "Pos",
    team: "Écurie",
    error: "Erreur",
    
    // Easter Egg
    easterEggTitle: "Easter Egg",
    easterEggPrompt: "Tape le",
    maxCode: "Max Code",
    easterEggSuffix: "sur ton clavier 🎮",
    boostActivated: "Boost activé ! Vroum vroum 🏎️💨",
    
    // Common
    loadingData: "Chargement...",
    defaultLoading: "Chargement...",
    
    // Footer
    footerDataProvided: "Données fournies par l'API Ergast F1",
    footerFrontCalls: "Front appelle",
    footerNotDefined: "N/D",
    footerProjectDescription: "Projet DevOps - Apprentissage",
    footerGitHub: "GitHub",
    footerCopyright: "copyright 2025 - Tous droits réservés - Louis BERTRAND",
  },
  en: {
    // Header
    appTitle: "F1 Dashboard",
    appSubtitle: "Real-time Formula 1 Statistics",
    apiLabel: "API",
    apiUndefined: "not defined",
    
    // Navigation
    navHome: "Home",
    navDrivers: "Drivers",
    navConstructors: "Constructors",
    navStats: "Statistics",
    navSchedule: "Schedule",
    navAbout: "About",
    
    // Home page
    top3Drivers: "Top 3 Drivers",
    mode: "Mode",
    lastRace: "Last Race",
    nextRace: "Next Race",
    podium: "Podium",
    loading: "Loading dashboard...",
    networkError: "Network error",
    pageNotFound: "Page not found.",
    
    // About page
    aboutTitle: "About the Project",
    aboutDescription: "F1 Dashboard is a DevOps learning project: FastAPI (backend), React+Vite (frontend), Docker, CI/CD GitHub Actions, Trivy scans, images published on GHCR and deployed on Railway.",
    programmingLanguages: "🗣️ Programming Languages",
    backend: "Backend",
    frontend: "Frontend",
    technologies: "🧰 Technologies Used",
    devopsInfra: "🚀 DevOps & Infrastructure",
    architectureNote: "Architecture note:",
    architectureText: "No /api proxy — the frontend calls directly",
    apiUrl: "the API URL",
    
    // Driver Standings
    driversStandings: "Drivers Standings",
    position: "Position",
    driver: "Driver",
    constructor: "Constructor",
    points: "Points",
    wins: "Wins",
    
    // Constructor Standings
    constructorsStandings: "Constructors Standings",
    
    // Schedule
    schedule: "Schedule",
    round: "Round",
    grandPrix: "Grand Prix",
    circuit: "Circuit",
    location: "Location",
    date: "Date",
    scheduleTitle: "Season Schedule",
    loadingSchedule: "Loading schedule...",
    
    // Pilot Stats
    pilotStats: "Driver Statistics",
    nationality: "Nationality",
    permanentNumber: "Permanent Number",
    code: "Code",
    sortBy: "Sort by:",
    minimum: "Minimum:",
    reset: "Reset",
    loadingStats: "Loading statistics...",
    poles: "Pole Positions",
    podiums: "Podiums",
    races: "Races",
    noDrivers: "No drivers match the filtering criteria.",
    
    // Drivers/Constructors Standings
    loadingDrivers: "Loading drivers standings...",
    loadingConstructors: "Loading constructors standings...",
    pos: "Pos",
    team: "Team",
    error: "Error",
    
    // Easter Egg
    easterEggTitle: "Easter Egg",
    easterEggPrompt: "Type the",
    maxCode: "Max Code",
    easterEggSuffix: "on your keyboard 🎮",
    boostActivated: "Boost activated! Vroom vroom 🏎️💨",
    
    // Common
    loadingData: "Loading...",
    defaultLoading: "Loading...",
    
    // Footer
    footerDataProvided: "Data provided by Ergast F1 API",
    footerFrontCalls: "Frontend calls",
    footerNotDefined: "N/A",
    footerProjectDescription: "DevOps Learning Project",
    footerGitHub: "GitHub",
    footerCopyright: "copyright 2025 - All rights reserved - Louis BERTRAND",
  }
};

export const useTranslation = (language) => {
  return (key) => {
    return translations[language]?.[key] || key;
  };
};
