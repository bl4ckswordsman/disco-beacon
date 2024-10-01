import { type RequestHandler } from "@sveltejs/kit";
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

  switch (action) {
    case "encrypt":
    case "decrypt":
      return typeof data === "string";
    case "send":
      return (
        typeof data === "object" &&
        "url" in data &&
        typeof data.url === "string" &&
        "payload" in data
      );
    default:
      return false;
  }
}

function createJsonResponse(
  data: Record<string, unknown>,
  status: number,
): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body: unknown = await request.json();

    if (!isWebhookRequest(body)) {
      return createJsonResponse({ error: "Invalid request format" }, 400);
    }

    switch (body.action) {
      case "encrypt": {
        const encryptedUrl = encrypt(body.data, DISCORDWEBHOOK_ENCRYPTION_KEY);
        return createJsonResponse({ encryptedUrl }, 200);
      }
      case "decrypt": {
        const decryptedUrl = decrypt(body.data, DISCORDWEBHOOK_ENCRYPTION_KEY);
        return createJsonResponse({ decryptedUrl }, 200);
      }
      case "send": {
        const decryptedUrl = decrypt(
          body.data.url,
          DISCORDWEBHOOK_ENCRYPTION_KEY,
        );
        if (typeof decryptedUrl !== "string") {
          throw new Error("Invalid decrypted URL");
        }
        const response = await fetch(decryptedUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body.data.payload),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return createJsonResponse({ success: true }, 200);
      }
    }
  } catch (error) {
    console.error("Error processing webhook request:", error);
    return createJsonResponse(
      {
        error: error instanceof Error ? error.message : "Internal server error",
      },
      500,
    );
  }
};
