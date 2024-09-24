<script lang="ts">
    export let message: string;
    export let type: "info" | "success" | "error" = "info";
</script>

<div class="toast toast-bottom toast-center z-[9999]">
    <div class="alert alert-{type}">
        <span>{message}</span>
    </div>
</div>
