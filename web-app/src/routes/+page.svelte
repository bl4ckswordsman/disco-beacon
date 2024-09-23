<script lang="ts">
    import NotificationButton from "$lib/components/NotificationButton.svelte";
    import SettingsView from "$lib/components/SettingsView.svelte";
    import Metadata from "$lib/components/Metadata.svelte";

    let showSettings = false;

    function toggleSettings() {
        showSettings = !showSettings;
    }
</script>

<Metadata
    title="Disco Beacon - Home"
    description="Send notifications about to your Discord server"
/>

<main class="font-sans text-center pt-12">
    <h1>Valheim Server Notifier</h1>
    <div class="m-2">
        {#if showSettings}
            <SettingsView />
        {:else}
            <NotificationButton />
        {/if}
        <button class="btn" on:click={toggleSettings}>
            {showSettings ? "Back to Notifier" : "Settings"}
        </button>
    </div>
</main>
