import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    hmr: {
      // Ensure HMR WebSocket uses the correct host
      host: 'localhost',
      port: 5173
    }
  }
})
