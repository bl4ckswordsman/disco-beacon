import { LOCAL_STORAGE_DISCORD_KEY } from "$lib/constants";

export function getStoredWebhookUrl(): string {
  if (typeof localStorage !== "undefined") {
    const storedValue = localStorage.getItem(
      LOCAL_STORAGE_DISCORD_KEY as string,
    ) as string | null;
    return storedValue ?? "";
  }
  return "";
}

export function setStoredWebhookUrl(url: string): void {
  if (typeof localStorage !== "undefined") {
    localStorage.setItem(LOCAL_STORAGE_DISCORD_KEY as string, url);
  }
}
