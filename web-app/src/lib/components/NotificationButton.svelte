<script lang="ts">
    import { webhookUrl } from "$lib/stores/settings-store";
    import { sendWebhookNotification } from "$lib/services/webhook-service";
    import type { WebhookPayload } from "$lib/types";
    import { toast } from "$lib/stores/toast-store";

    async function sendNotification() {
        if (!$webhookUrl) {
            toast.show("Error: Webhook URL not set", "error");
            return;
        }

        toast.show("Sending notification...", "info");

        const payload: WebhookPayload = {
            content: "The Valheim server is up. @everyone",
            embeds: [
                {
                    title: "Server Status",
                    description: "Valheim server is now online!",
                    color: 5763719,
                },
            ],
        };

        try {
            const success = await sendWebhookNotification($webhookUrl, payload);
            toast.show(
                success
                    ? "Notification sent successfully!"
                    : "Error: Failed to send notification",
                success ? "success" : "error",
            );
        } catch (error) {
            toast.show(
                error instanceof Error
                    ? `Error: ${error.message}`
                    : "Error: An unknown error occurred",
                "error",
            );
        }
    }
</script>

<button class="btn btn-lg btn-wide" on:click={sendNotification}>
    Notify Discord
</button>
