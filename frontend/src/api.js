import axios from "axios";

export const API_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

export const api = axios.create({
  baseURL: API_URL,
  timeout: 15000,
  headers: { "X-Requested-With": "XMLHttpRequest" },
});

// helpers sûrs
export const getDrivers = async () => {
  const { data } = await api.get("/drivers/current");
  return Array.isArray(data) ? data : [];
};

export const getDriverStandings = async () => {
  const { data } = await api.get("/standings/drivers");
  // data = tableau côté mock, sinon on tente de normaliser
  if (Array.isArray(data)) return data;
  return data?.MRData?.StandingsTable?.StandingsLists?.[0]?.DriverStandings ?? [];
};

export const getConstructorStandings = async () => {
  const { data } = await api.get("/standings/constructors");
  if (Array.isArray(data)) return data;
  return data?.MRData?.StandingsTable?.StandingsLists?.[0]?.ConstructorStandings ?? [];
};

export const getSchedule = async () => {
  const { data } = await api.get("/schedule/current");
  return Array.isArray(data) ? data : [];
};

export const getHealth = async () => {
  const { data } = await api.get("/health");
  return data;
};

export const getRaceResult = async (season, round) => {
  try {
    const { data } = await api.get(`/race/${season}/${round}`);
    return data;
  } catch (error) {
    if (error.response?.status === 404) {
      return null; // Race results not available
    }
    throw error;
  }
};

export const getLastRace = async () => {
  try {
    const { data } = await api.get("/race/last");
    return data;
  } catch (error) {
    console.error("Error fetching last race:", error);
    return null;
  }
};

export const getAllDriverStats = async () => {
  const { data } = await api.get("/drivers/stats");
  return Array.isArray(data) ? data : [];
};
