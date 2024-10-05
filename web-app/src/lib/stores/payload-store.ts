import { writable } from "svelte/store";
import type { WebhookPayload } from "$lib/types";

const defaultPayload: WebhookPayload = {
  content: "The Valheim server is up. @everyone",
  embeds: [
    {
      title: "Server Status",
      description: "Valheim server is now online!",
      color: 5763719,
    },
  ],
};

export const webhookPayload = writable<WebhookPayload>(defaultPayload);
