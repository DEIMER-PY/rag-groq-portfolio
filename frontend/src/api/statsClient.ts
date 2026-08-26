import { API_URL } from "../config";
import type { Stats } from "../types/stats";

export async function fetchStats(): Promise<Stats> {
  const response = await fetch(`${API_URL}/stats`);
  if (!response.ok) {
    throw new Error(`Error ${response.status} al obtener estadísticas`);
  }
  return response.json();
}
