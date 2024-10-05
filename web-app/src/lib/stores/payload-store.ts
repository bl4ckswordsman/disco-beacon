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
const typedWritable = writable as <T>(_value: T) => {
  subscribe: (_run: (value: T) => void) => () => void;
  set: (_value: T) => void;
  update: (_updater: (value: T) => T) => void;
};

export const webhookPayload = typedWritable(defaultPayload);
