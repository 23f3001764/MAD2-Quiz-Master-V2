import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
// import vueDevTools from 'vite-plugin-vue-devtools'; // Uncomment if needed

export default defineConfig({
  plugins: [
    vue(),
    // vueDevTools() // Uncomment this if you want to use Vue DevTools
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        // rewrite: path => path.replace(/^\/api/, '') // Ensures API requests are correctly forwarded
      }
    }
  },
  assetsInclude: ['**/*.{JPG,jpg,png,svg}'] // Supports additional image formats
});
