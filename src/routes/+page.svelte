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

<main class="font-sans text-center pt-12">
    <h1>Valheim Server Notifier</h1>
    <div class="m-2">
        {#if showSettings}
            <SettingsView {webhookUrl} on:update={e => updateWebhookUrl(e.detail)}/>
        {:else}
            <NotificationButton {webhookUrl}/>
        {/if}
        <button class="btn" on:click={toggleSettings}>
            {showSettings ? 'Back to Notifier' : 'Settings'}
        </button>

<!--        <div class="flex justify-center mb-5 pt-16">
            <GitHubBadges owner="bl4ckswordsman" repo="discord-beacon"/>
        </div>-->
    </div>
</main>
