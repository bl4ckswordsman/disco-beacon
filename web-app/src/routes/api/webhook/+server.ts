import { json, type RequestHandler } from "@sveltejs/kit";
import { DISCORDWEBHOOK_ENCRYPTION_KEY } from "$env/static/private";
import { encrypt, decrypt } from "$lib/server/crypto";

interface EncryptRequest {
  action: "encrypt";
  data: string;
}

interface DecryptRequest {
  action: "decrypt";
  data: string;
}

interface SendRequest {
  action: "send";
  data: {
    url: string;
    payload: unknown;
  };
}

type WebhookRequest = EncryptRequest | DecryptRequest | SendRequest;

function isWebhookRequest(obj: unknown): obj is WebhookRequest {
  if (typeof obj !== "object" || obj === null) return false;
  const { action, data } = obj as Partial<WebhookRequest>;
  if (typeof action !== "string") return false;
  if (!["encrypt", "decrypt", "send"].includes(action)) return false;
  if (typeof data !== "string" && typeof data !== "object") return false;
  if (action === "send" && typeof data === "object") {
    const { url, payload } = data as Partial<SendRequest["data"]>;
    return typeof url === "string" && payload !== undefined;
  }
  return true;
}

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body: unknown = await request.json();

    if (!isWebhookRequest(body)) {
      return json({ error: "Invalid request format" }, { status: 400 });
    }

    switch (body.action) {
      case "encrypt": {
        const encryptedUrl = encrypt(body.data, DISCORDWEBHOOK_ENCRYPTION_KEY);
        return json({ encryptedUrl });
      }
      case "decrypt": {
        const decryptedUrl = decrypt(body.data, DISCORDWEBHOOK_ENCRYPTION_KEY);
        return json({ decryptedUrl });
      }
      case "send": {
        const decryptedUrl = decrypt(
          body.data.url,
          DISCORDWEBHOOK_ENCRYPTION_KEY,
        );
        const response = await fetch(decryptedUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body.data.payload),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return json({ success: true });
      }
    }
  } catch (error) {
    console.error("Error processing webhook request:", error);
    if (error instanceof Error) {
      return json({ error: error.message }, { status: 500 });
    }
    return json({ error: "Internal server error" }, { status: 500 });
  }
};
