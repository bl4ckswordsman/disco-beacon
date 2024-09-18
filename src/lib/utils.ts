export function getStoredWebhookUrl(): string {
    if (typeof localStorage !== 'undefined') {
        return localStorage.getItem("discordWebhookUrl") || "";
    }
    return "";
}

export function setStoredWebhookUrl(url: string): void {
    if (typeof localStorage !== 'undefined') {
        localStorage.setItem("discordWebhookUrl", url);
    }
}