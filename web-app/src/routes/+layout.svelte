<script lang="ts">
    import "../app.css";
    import Navbar from "$lib/components/Navbar.svelte";
    import Footer from "$lib/components/Footer.svelte";
    import { GITHUB } from "$lib/constants";
    import { toast } from "$lib/stores/toast-store";
    import Toast from "$lib/components/Toast.svelte";

    const githubLink = `https://github.com/${GITHUB.USERNAME}/${GITHUB.REPO_NAME}`;
</script>

<div class="flex flex-col min-h-screen">
    <header>
        <Navbar {githubLink} />
    </header>
    <main class="flex-grow">
        <slot />
    </main>
    <Footer />

    {#if $toast}
        <Toast message={$toast.message} type={$toast.type} />
    {/if}
</div>
