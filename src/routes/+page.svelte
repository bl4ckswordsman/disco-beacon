<script lang="ts">
    import {onMount} from 'svelte';
    import NotificationButton from '$lib/components/NotificationButton.svelte';
    import SettingsView from '$lib/components/SettingsView.svelte';
    import GitHubBadges from "$lib/components/GitHubBadges.svelte";

    let showSettings = false;
    let webhookUrl = '';

    onMount(() => {
        const storedUrl = localStorage.getItem('discordWebhookUrl');
        if (storedUrl) {
            webhookUrl = storedUrl;
        }
    });

    function toggleSettings() {
        showSettings = !showSettings;
    }

    function updateWebhookUrl(newUrl: string) {
        webhookUrl = newUrl;
        localStorage.setItem('discordWebhookUrl', newUrl);
    }
</script>

<main>
    <h1>Valheim Server Notifier</h1>
    {#if showSettings}
        <SettingsView {webhookUrl} on:update={e => updateWebhookUrl(e.detail)}/>
    {:else}
        <NotificationButton {webhookUrl}/>
    {/if}
    <button on:click={toggleSettings}>
        {showSettings ? 'Back to Notifier' : 'Settings'}
    </button>
    <div class="badges-container">
        <GitHubBadges owner="bl4ckswordsman" repo="discord-beacon"/>
    </div>
</main>

<style>
    main {
        font-family: Arial, sans-serif;
        text-align: center;
        padding-top: 50px;
    }

    .badges-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
        padding-top: 70px;
    }
</style>