import { LOCAL_STORAGE_DISCORD_KEY } from "$lib/constants";

export function getStoredWebhookUrl(): string {
  if (typeof localStorage !== "undefined") {
    const storedValue = localStorage.getItem(LOCAL_STORAGE_DISCORD_KEY);
    return storedValue !== null ? storedValue : "";
  }
  return "";
}

export function setStoredWebhookUrl(url: string): void {
  if (typeof localStorage !== "undefined") {
    localStorage.setItem(LOCAL_STORAGE_DISCORD_KEY, url);
  }
}
