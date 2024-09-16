<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import KeyRound from "$assets/icons/KeyRound.svelte";

    export let webhookUrl: string;

    const dispatch = createEventDispatcher();
    let inputUrl = webhookUrl;

    function saveSettings() {
        dispatch("update", inputUrl);
    }
</script>

<div class="flex flex-col items-center gap-2.5">
    <h2>Settings</h2>
    <label for="webhook-url">Discord Webhook URL:</label>
    <label class="input input-bordered flex items-center gap-2">
        <KeyRound />
        <input
            id="webhook-url"
            type="password"
            bind:value={inputUrl}
            placeholder="Enter Discord webhook URL"
        />
    </label>
    <button class="btn" on:click={saveSettings}>Save</button>
</div>
