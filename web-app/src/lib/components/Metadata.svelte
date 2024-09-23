<script lang="ts">
    export let title = "Disco Beacon";
    export let description =
        "Svelte app for Discord notifications via webhooks";
</script>

<svelte:head>
    <title>{title}</title>
    <meta name="description" content={description} />
    <meta name="application-name" content={title} />
</svelte:head>
