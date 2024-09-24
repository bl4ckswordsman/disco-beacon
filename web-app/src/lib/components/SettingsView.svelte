<script lang="ts">
    import { webhookUrl } from "$lib/stores/settings-store";
    import { webhookPayload } from "$lib/stores/payload-store";
    import KeyRound from "$assets/icons/KeyRound.svelte";
    import { encryptWebhookUrl } from "$lib/services/webhook-service";
    import {toast} from "$lib/stores/toast-store";

    let inputUrl = $webhookUrl;
    let inputPayload = JSON.stringify($webhookPayload, null, 2);

    async function saveSettings(event: Event): Promise<void> {
        event.preventDefault();
        $webhookUrl = await encryptWebhookUrl(inputUrl);
        try {
            $webhookPayload = JSON.parse(inputPayload);
        } catch (error) {
            console.error("Invalid JSON for payload", error);
            toast.show("Error: Invalid JSON for payload", "error");
        }
    }
</script>

<h3 class="font-bold text-lg">Settings</h3>
<form on:submit={saveSettings} class="py-4">
    <label for="username" class="sr-only">Username</label>
    <input
        id="username"
        type="text"
        autocomplete="username"
        value="Discord Webhook URL"
        class="hidden"
    />
    <label for="webhook-url" class="label">Discord Webhook URL:</label>
    <label class="input input-bordered flex items-center gap-2">
        <KeyRound />
        <input
            id="webhook-url"
            type="password"
            bind:value={inputUrl}
            placeholder="Enter Discord webhook URL"
            autocomplete="new-password"
            class="w-full"
        />
    </label>
    <label for="webhook-payload" class="label">Webhook Payload:</label>
    <textarea
        id="webhook-payload"
        bind:value={inputPayload}
        rows="10"
        class="textarea textarea-bordered w-full"
        placeholder="Enter JSON payload"
    ></textarea>

    <div class="modal-action">
        <button type="submit" class="btn btn-primary">Save</button>
    </div>
</form>
