<script>
    import "../app.css";
</script>

<div class="flex flex-col min-h-screen">
    <main class="flex-grow">
        <slot />
    </main>
    <footer class="footer footer-center p-4 mt-4">
        <div class="container mx-auto text-center">
            © {new Date().getFullYear()} bl4ckswordsman
        </div>
    </footer>
</div>
