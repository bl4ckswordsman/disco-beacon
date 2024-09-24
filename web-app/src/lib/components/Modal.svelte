<script lang="ts">
    export let isOpen: boolean;
    export let onClose: () => void;
</script>

<dialog class="modal modal-bottom sm:modal-middle" class:modal-open={isOpen}>
    <div class="modal-box">
        <slot />
        <div class="modal-action">
            <button class="btn" on:click={onClose}>Close</button>
        </div>
    </div>
</dialog>
