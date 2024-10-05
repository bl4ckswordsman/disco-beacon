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

const typedWritable = writable as <T>(value: T) => {
  subscribe: (run: (value: T) => void) => () => void;
  set: (value: T) => void;
  update: (updater: (value: T) => T) => void;
};

export const webhookPayload = typedWritable(defaultPayload);
