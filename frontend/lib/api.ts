import { EventInput, SampleEvent, SimulationResponse } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

export async function fetchSampleEvents(): Promise<SampleEvent[]> {
  const res = await fetch(`${API_BASE_URL}/sample-events`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error("Failed to load sample events");
  }
  return res.json();
}

export async function simulateEvent(payload: EventInput): Promise<SimulationResponse> {
  const res = await fetch(`${API_BASE_URL}/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || "Simulation request failed");
  }

  return res.json();
}
