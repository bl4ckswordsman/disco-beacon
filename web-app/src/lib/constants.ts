export const ENCRYPTION_ALGORITHM = "aes-256-cbc";
export const DISCORD_API_ENDPOINT: string = "/api/webhook";
export const LOCAL_STORAGE_DISCORD_KEY = "discordWebhookUrl";

export const PROJECT_INFO = {
  TITLE: "Disco Beacon",
  DESCRIPTION: "Svelte app for Discord notifications via webhooks",
} as const;

export const GITHUB = {
  USERNAME: "bl4ckswordsman",
  REPO_NAME: "disco-beacon",
} as const;
