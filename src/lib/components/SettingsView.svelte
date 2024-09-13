<script lang="ts">
    import {createEventDispatcher} from 'svelte';

    export let webhookUrl: string;

    const dispatch = createEventDispatcher();
    let inputUrl = webhookUrl;

    function saveSettings() {
        dispatch('update', inputUrl);
    }
</script>

<div>
    <h2>Settings</h2>
    <label for="webhook-url">Discord Webhook URL:</label>
    <input
            id="webhook-url"
            type="text"
            bind:value={inputUrl}
            placeholder="Enter Discord webhook URL"
    />
    <button on:click={saveSettings}>Save</button>
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }

    input {
        width: 300px;
        padding: 5px;
    }
</style>