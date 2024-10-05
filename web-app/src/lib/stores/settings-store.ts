import { writable, type Writable } from "svelte/store";
import { getStoredWebhookUrl, setStoredWebhookUrl } from "$lib/utils";
export const webhookUrl = writable<string>(getStoredWebhookUrl() as string);

(webhookUrl as Writable<string>).subscribe((value: string) => {
  try {
    setStoredWebhookUrl(value);
  } catch (error) {
    console.error("Failed to set stored webhook URL:", error);
  }
});
