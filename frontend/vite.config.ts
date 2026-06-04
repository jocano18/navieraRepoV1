import path from 'node:path';
import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

/** Backend URL for Vite dev proxy (Docker: http://backend:8000). */
const apiProxyTarget = process.env.VITE_PROXY_TARGET ?? 'http://localhost:8000';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/health': { target: apiProxyTarget, changeOrigin: true },
      '/inbox': { target: apiProxyTarget, changeOrigin: true },
      '/shipments': { target: apiProxyTarget, changeOrigin: true },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/testing/setup.ts'],
    css: true,
    env: {
      VITE_API_URL: 'http://localhost:8000',
    },
  },
});
