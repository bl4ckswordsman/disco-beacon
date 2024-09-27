import { WebhookAction, type WebhookPayload } from "$lib/types";
import { DISCORD_API_ENDPOINT } from "$lib/constants";

interface EncryptResponse {
  encryptedUrl: string;
}

interface SendResponse {
  success?: boolean;
}

export async function encryptWebhookUrl(url: string): Promise<string> {
  try {
    const response = await fetch(DISCORD_API_ENDPOINT as string, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: WebhookAction.Encrypt,
        data: url,
      }),
    });
    if (!response.ok) {
      throw new Error(
        `Failed to encrypt webhook URL: HTTP status ${response.status}`,
      );
    }
    const result = (await response.json()) as EncryptResponse;
    if (!result.encryptedUrl) {
      throw new Error("Encrypted URL is missing in the response");
    }
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
    const response = await fetch(DISCORD_API_ENDPOINT as string, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: WebhookAction.Send as WebhookAction.Send,
        data: { url: encryptedWebhookUrl, payload },
      }),
    });
    if (!response.ok) {
      throw new Error( //TODO: Fix warning ('throw' of exception caught locally)
        `Failed to send webhook notification: HTTP status ${response.status}`,
      );
    }
    const result = (await response.json()) as { success?: boolean };
    return result.success ?? false;
  } catch (error) {
    console.error("Error occurred while sending webhook notification:", error);
    throw error;
  }
}
