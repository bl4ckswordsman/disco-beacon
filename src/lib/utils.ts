import {LOCAL_STORAGE_DISCORD_KEY} from "$lib/constants";

export function getStoredWebhookUrl(): string {
    if (typeof localStorage !== 'undefined') {
        return localStorage.getItem(LOCAL_STORAGE_DISCORD_KEY) || "";
    }
    return "";
}

export function setStoredWebhookUrl(url: string): void {
    if (typeof localStorage !== 'undefined') {
        localStorage.setItem(LOCAL_STORAGE_DISCORD_KEY, url);
    }
}