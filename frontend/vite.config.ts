import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';


// ============================================================
// VITE CONFIGURATION
// ============================================================

export default defineConfig({

  // ==========================================================
  // REACT PLUGIN
  // ==========================================================

  // Enables React and TypeScript support in Vite.
  plugins: [react()],


  // ==========================================================
  // DEVELOPMENT SERVER
  // ==========================================================

  server: {

    // --------------------------------------------------------
    // FLASK API PROXY
    // --------------------------------------------------------

    // The frontend uses:
    //
    //     fetch('/predict')
    //
    // Instead of sending that request to Vite itself,
    // Vite forwards it to our Flask backend running on
    // localhost:5000.
    proxy: {

      '/predict': {

        // Flask development server.
        target: 'http://127.0.0.1:5000',

        // Makes the request appear to Flask as if it
        // originated from the same host.
        changeOrigin: true

      }

    }

  }

});