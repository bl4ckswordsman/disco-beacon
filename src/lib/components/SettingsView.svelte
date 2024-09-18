<script lang="ts">
    import { webhookUrl } from "$lib/stores/settings-store";
    import KeyRound from "$assets/icons/KeyRound.svelte";

    let inputUrl = $webhookUrl;

    function saveSettings() {
        $webhookUrl = inputUrl;
    }
</script>

<div class="flex flex-col items-center gap-2.5">
    <h2>Settings</h2>
    <form on:submit={saveSettings} class="flex flex-col items-center gap-2.5">
        <label for="username" class="sr-only">Username</label>
        <input
            id="username"
            type="text"
            autocomplete="username"
            value="Discord Webhook URL"
            class="hidden"
        />
        <label for="webhook-url">Discord Webhook URL:</label>
        <label class="input input-bordered flex items-center gap-2">
            <KeyRound />
            <input
                id="webhook-url"
                type="password"
                bind:value={inputUrl}
                placeholder="Enter Discord webhook URL"
                autocomplete="new-password"
            />
        </label>
        <button type="submit" class="btn">Save</button>
    </form>
</div>
