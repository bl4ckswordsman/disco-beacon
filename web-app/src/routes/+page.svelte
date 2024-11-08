<script lang="ts">
    import NotificationButton from "$lib/components/NotificationButton.svelte";
    import SettingsView from "$lib/components/SettingsView.svelte";
    import Modal from "$lib/components/Modal.svelte";
    import Metadata from "$lib/components/Metadata.svelte";

    let title: string = "Disco Beacon";
    let description: string = "Send notifications to your Discord server";

    let isSettingsOpen = false;

    function toggleSettings() {
        isSettingsOpen = !isSettingsOpen;
    }
</script>

<Metadata {title} {description} />

<main class="font-sans text-center max-w-2xl mx-auto pt-12">
    <div class="m-2">
        <NotificationButton />
    </div>
    <button class="btn btn-neutral m-2" on:click={toggleSettings}
        >Settings</button
    >
</main>

<Modal isOpen={isSettingsOpen} onClose={toggleSettings}>
    <SettingsView />
</Modal>
