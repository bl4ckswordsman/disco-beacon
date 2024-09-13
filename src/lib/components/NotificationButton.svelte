<script lang="ts">
    export let webhookUrl: string;

    let status = '';

    async function sendNotification() {
        if (!webhookUrl) {
            status = 'Error: Webhook URL not set';
            return;
        }

        status = 'Sending notification...';

        try {
            const response = await fetch(webhookUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: 'The Valheim server is up. @everyone',
                    embeds: [{
                        title: 'Server Status',
                        description: 'Valheim server is now online!',
                        color: 5763719 // Green color
                    }]
                })
            });

            if (response.ok) {
                status = 'Notification sent successfully!';
            } else {
                status = 'Error: Failed to send notification';
            }
        } catch (error) {
            if (error instanceof Error) {
                status = `Error: ${error.message}`;
            } else {
                status = 'Error: An unknown error occurred';
            }
        }
    }
</script>

<button on:click={sendNotification}>Notify Discord</button>
<p>{status}</p>

<style>
    button {
        font-size: 24px;
        padding: 15px 30px;
    }
</style>