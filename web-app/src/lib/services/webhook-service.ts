import { WebhookAction, type WebhookPayload } from "$lib/types";
import { DISCORD_API_ENDPOINT } from "$lib/constants";

export async function encryptWebhookUrl(url: string): Promise<string> {
  try {
    const response = await fetch(DISCORD_API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: WebhookAction.Encrypt, data: url }),
    });
    if (!response.ok) {
      throw new Error(
        `Failed to encrypt webhook URL: HTTP status ${response.status}`,
      );
    }
    const result = await response.json();
    return result.encryptedUrl;
  } catch (error) {
    console.error("Error occurred while encrypting webhook URL:", error);
    if (error instanceof Error) {
      throw new Error(`Encryption failed: ${error.message}`);
    } else {
      throw new Error("Encryption failed: An unknown error occurred");
    }
  }
}

export async function sendWebhookNotification(
  encryptedWebhookUrl: string,
  payload: WebhookPayload,
): Promise<boolean> {
  try {
    const response = await fetch(DISCORD_API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: WebhookAction.Send,
        data: { url: encryptedWebhookUrl, payload },
      }),
    });
    if (!response.ok) {
      throw new Error( //TODO: Fix warning ('throw' of exception caught locally)
        `Failed to send webhook notification: HTTP status ${response.status}`,
      );
    }
    const result = await response.json();
    return result.success;
  } catch (error) {
    console.error("Error occurred while sending webhook notification:", error);
    if (error instanceof Error) {
      throw new Error(`Notification failed: ${error.message}`);
    } else {
      throw new Error("Notification failed: An unknown error occurred");
    }
  }
}