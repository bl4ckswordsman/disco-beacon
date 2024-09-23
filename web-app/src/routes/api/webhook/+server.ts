import { json } from "@sveltejs/kit";
import { DISCORDWEBHOOK_ENCRYPTION_KEY } from "$env/static/private";
import { encrypt, decrypt } from "$lib/server/crypto";
import type { RequestHandler } from "./$types";

export const POST: RequestHandler = async ({ request }) => {
  const { action, data } = await request.json();

  switch (action) {
    case "encrypt":
      return json({
        encryptedUrl: encrypt(data, DISCORDWEBHOOK_ENCRYPTION_KEY),
      });
    case "decrypt":
      return json({
        decryptedUrl: decrypt(data, DISCORDWEBHOOK_ENCRYPTION_KEY),
      });
    case "send":
      const decryptedUrl = decrypt(data.url, DISCORDWEBHOOK_ENCRYPTION_KEY);
      const response = await fetch(decryptedUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data.payload),
      });
      return json({ success: response.ok });
    default:
      return json({ error: "Invalid action" }, { status: 400 });
  }
};
