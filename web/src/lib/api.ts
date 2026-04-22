export async function getHealth(): Promise<{ status: string; workspace: string }> {
  const response = await fetch("/api/health");
  if (!response.ok) {
    throw new Error("health request failed");
  }
  return response.json();
}
