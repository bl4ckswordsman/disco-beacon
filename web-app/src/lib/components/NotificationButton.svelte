<script lang="ts">
    import { webhookUrl } from "$lib/stores/settings-store";
    import { sendWebhookNotification } from "$lib/services/webhook-service";
    import { webhookPayload } from "$lib/stores/payload-store";
    import { toast } from "$lib/stores/toast-store";

    async function sendNotification() {
        if (!$webhookUrl) {
            toast.show("Error: Webhook URL not set", "error");
            return;
        }

        toast.show("Sending notification...", "info");

        try {
            const success = await sendWebhookNotification(
                $webhookUrl,
                $webhookPayload,
            );
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
