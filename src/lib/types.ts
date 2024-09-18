export interface WebhookPayload {
  content: string;
  embeds: Array<{
    title: string;
    description: string;
    color: number;
  }>;
}

export enum WebhookAction {
  Encrypt = "encrypt",
  Send = "send",
}
