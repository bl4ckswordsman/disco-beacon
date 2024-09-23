<script lang="ts">
    import { PROJECT_INFO } from "$lib/constants";

    export let title: string = PROJECT_INFO.TITLE;
    export let description: string = PROJECT_INFO.DESCRIPTION;
</script>

<svelte:head>
    <title>{title}</title>
    <meta name="description" content={description} />
    <meta name="application-name" content={title} />
</svelte:head>
