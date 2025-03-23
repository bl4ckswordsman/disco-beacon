<script lang="ts">
    import GitHub from "$assets/icons/GitHub.svelte";

    export let githubLink: string;
</script>

<div class="navbar bg-base-100 max-w-2xl mx-auto">
    <div class="flex-1">
        <a href="/" class="btn btn-ghost text-xl">Disco Beacon</a>
    </div>
    <div class="flex-none">
        <a
            href={githubLink}
            target="_blank"
            rel="noopener noreferrer"
            class="btn btn-square btn-ghost"
            aria-label="GitHub Repository link"
        >
            <GitHub />
        </a>
    </div>
</div>
