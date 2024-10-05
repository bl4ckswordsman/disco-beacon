import { writable, type Writable } from "svelte/store";
import { getStoredWebhookUrl, setStoredWebhookUrl } from "$lib/utils";

export const webhookUrl: Writable<string> = writable(getStoredWebhookUrl());

webhookUrl.subscribe((value) => {
  try {
    setStoredWebhookUrl(value);
  } catch (error) {
    console.error("Failed to set stored webhook URL:", error);
  }
});
