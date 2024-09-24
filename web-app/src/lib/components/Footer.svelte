<script lang="ts">
    import { GITHUB } from "$lib/constants";

    export let footerText = GITHUB.USERNAME;
</script>

<footer class="footer footer-center p-4 mt-4">
    <div class="container mx-auto text-center">
        © {new Date().getFullYear()}
        {footerText}
    </div>
</footer>
