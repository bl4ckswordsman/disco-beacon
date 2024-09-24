<script lang="ts">
    import { webhookUrl } from "$lib/stores/settings-store";
    import KeyRound from "$assets/icons/KeyRound.svelte";
    import { encryptWebhookUrl } from "$lib/services/webhook-service";

    let inputUrl = $webhookUrl;

    async function saveSettings(event: Event): Promise<void> {
        event.preventDefault();
        $webhookUrl = await encryptWebhookUrl(inputUrl);
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
    <div class="modal-action">
        <button type="submit" class="btn btn-primary">Save</button>
    </div>
</form>
