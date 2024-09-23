<script>
    import "../app.css";
    import Navbar from "$lib/components/Navbar.svelte";
    import { GITHUB } from "$lib/constants";

    const githubLink =
        "https://github.com/" + GITHUB.USERNAME + "/" + GITHUB.REPO_NAME;
    let footerText = GITHUB.USERNAME;
</script>

<div class="flex flex-col min-h-screen">
    <header>
        <Navbar {githubLink} />
    </header>
    <main class="flex-grow">
        <slot />
    </main>
    <footer class="footer footer-center p-4 mt-4">
        <div class="container mx-auto text-center">
            © {new Date().getFullYear()}
            {footerText}
        </div>
    </footer>
</div>
