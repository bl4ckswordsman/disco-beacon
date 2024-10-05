import { writable } from "svelte/store";
import { getStoredWebhookUrl, setStoredWebhookUrl } from "$lib/utils";
export const webhookUrl = writable<string>(getStoredWebhookUrl() as string);

(
  webhookUrl as { subscribe: (callback: (value: string) => void) => void }
).subscribe((value) => {
  try {
    setStoredWebhookUrl(value);
  } catch (error) {
    console.error("Failed to set stored webhook URL:", error);
  }
});
