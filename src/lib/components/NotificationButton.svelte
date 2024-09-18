<script lang="ts">
    import { webhookUrl } from "$lib/stores/settings-store";
    import { sendWebhookNotification } from "$lib/services/webhook-service";
    import type { WebhookPayload } from "$lib/types";

    let status = "";

    async function sendNotification() {
        if (!$webhookUrl) {
            status = "Error: Webhook URL not set";
            return;
        }

        status = "Sending notification...";

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
            const response = await sendWebhookNotification(
                $webhookUrl,
                payload,
            );
            status = response.ok
                ? "Notification sent successfully!"
                : "Error: Failed to send notification";
        } catch (error) {
            status =
                error instanceof Error
                    ? `Error: ${error.message}`
                    : "Error: An unknown error occurred";
        }
    }
</script>

<button class="btn btn-lg btn-wide" on:click={sendNotification}
    >Notify Discord</button
>
<p>{status}</p>
