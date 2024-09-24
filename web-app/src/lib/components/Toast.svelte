<script lang="ts">
    export let message: string;
    export let type: "info" | "success" | "error" = "info";
</script>

<div class="toast toast-bottom toast-center">
    <div class="alert alert-{type}">
        <span>{message}</span>
    </div>
</div>
