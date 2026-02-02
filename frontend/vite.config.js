import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Yahan tumhara Flask backend ka URL daloge
        changeOrigin: true,
      }
    }
  }
})