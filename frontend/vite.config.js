import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    host: '0.0.0.0',
    port: 12001,
    strictPort: false,
    cors: true,
    hmr: {
      clientPort: 443,
      host: '0.0.0.0',
    },
    watch: {
      usePolling: true,
    },
    allowedHosts: true, // Allow all hosts
  },
});