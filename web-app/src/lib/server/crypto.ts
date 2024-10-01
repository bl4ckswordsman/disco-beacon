import * as crypto from "crypto";
import { ENCRYPTION_ALGORITHM } from "$lib/constants";

function hexToBuffer(hex: string): Buffer {
  return Buffer.from(hex, "hex");
}

export function encrypt(text: string, key: string): string {
  const iv: Buffer = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(
    ENCRYPTION_ALGORITHM as crypto.CipherGCMTypes,
    hexToBuffer(key),
    iv,
  );
  let encrypted = cipher.update(text, "utf8", "hex");
  encrypted += cipher.final("hex");
  return iv.toString("hex") + ":" + encrypted;
}

export function decrypt(text: string, key: string): string {
  const textParts: string[] = text.split(":");
  const iv: Buffer = Buffer.from(textParts.shift() ?? "", "hex");
  const encryptedText: string = textParts.join(":");
  const decipher = crypto.createDecipheriv(
    ENCRYPTION_ALGORITHM as crypto.CipherGCMTypes,
    hexToBuffer(key),
    iv,
  );
  let decrypted = decipher.update(encryptedText, "hex", "utf8");
  decrypted += decipher.final("utf8");
  return decrypted;
}
