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

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body = (await request.json()) as WebhookRequest;

    switch (body.action) {
      case "encrypt":
        return json({
          encryptedUrl: encrypt(body.data, DISCORDWEBHOOK_ENCRYPTION_KEY),
        });
      case "decrypt":
        return json({
          decryptedUrl: decrypt(body.data, DISCORDWEBHOOK_ENCRYPTION_KEY),
        });
      case "send":
        const decryptedUrl = decrypt(
          body.data.url,
          DISCORDWEBHOOK_ENCRYPTION_KEY,
        );
        const response = await fetch(decryptedUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body.data.payload),
        });
        return json({ success: response.ok });
      default:
        return json({ error: "Invalid action" }, { status: 400 });
    }
  } catch (error) {
    console.error("Error processing webhook request:", error);
    return json({ error: "Internal server error" }, { status: 500 });
  }
};
