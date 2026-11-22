// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://saibodanfakha.com',
  // /demarrer/ : questionnaire client, noindex et hors sitemap (22/11/2026).
  integrations: [sitemap({ filter: (page) => !page.includes('/demarrer/') })],
  vite: {
    plugins: [tailwindcss()]
  }
});