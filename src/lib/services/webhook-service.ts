import type { WebhookPayload } from "$lib/types";

export async function sendWebhookNotification(
  webhookUrl: string,
  payload: WebhookPayload,
): Promise<Response> {
  return fetch(webhookUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}
