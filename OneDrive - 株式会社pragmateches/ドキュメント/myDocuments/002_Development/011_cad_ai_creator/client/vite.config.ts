import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['pyodide']
  },
  build: {
    commonjsOptions: {
      include: [/fabric/, /node_modules/]
    }
  }
});