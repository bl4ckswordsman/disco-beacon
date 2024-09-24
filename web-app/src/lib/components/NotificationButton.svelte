<script lang="ts">
    import { webhookUrl } from "$lib/stores/settings-store";
    import { sendWebhookNotification } from "$lib/services/webhook-service";
    import type { WebhookPayload } from "$lib/types";
    import Toast from "$lib/components/Toast.svelte";

    let showToast = false;
    let toastMessage = "";
    let toastType: "info" | "success" | "error" = "info";

    function displayToast(message: string, type: "info" | "success" | "error") {
        toastMessage = message;
        toastType = type;
        showToast = true;
        setTimeout(() => {
            showToast = false;
        }, 3000);
    }

    async function sendNotification() {
        if (!$webhookUrl) {
            displayToast("Error: Webhook URL not set", "error");
            return;
        }

        displayToast("Sending notification...", "info");

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
            displayToast(
                success
                    ? "Notification sent successfully!"
                    : "Error: Failed to send notification",
                success ? "success" : "error",
            );
        } catch (error) {
            displayToast(
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

{#if showToast}
    <Toast message={toastMessage} type={toastType} />
{/if}
