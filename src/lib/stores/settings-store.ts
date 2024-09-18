import { writable } from "svelte/store";
import { getStoredWebhookUrl, setStoredWebhookUrl } from "$lib/utils";

export const webhookUrl = writable(getStoredWebhookUrl());

webhookUrl.subscribe((value) => {
  setStoredWebhookUrl(value);
});
