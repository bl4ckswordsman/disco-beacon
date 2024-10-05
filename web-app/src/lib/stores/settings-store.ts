import { writable } from "svelte/store";
import type { Writable } from "svelte/store";
import { getStoredWebhookUrl, setStoredWebhookUrl } from "$lib/utils";

const createWebhookUrlStore = (): Writable<string> => {
  const store = writable<string>(getStoredWebhookUrl());

  store.subscribe((value) => {
    try {
      setStoredWebhookUrl(value);
    } catch (error) {
      console.error("Failed to set stored webhook URL:", error);
    }
  });

  return store;
};

export const webhookUrl = createWebhookUrlStore();
