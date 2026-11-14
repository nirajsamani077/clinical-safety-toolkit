import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

// Pages are built as plain .html files with relative links (see scripts/relativise.mjs),
// so the same build works on GitHub Pages, a custom domain or a preview link.
export default defineConfig({
  integrations: [mdx()],
  build: {
    format: 'file',
    inlineStylesheets: 'always',
  },
  trailingSlash: 'never',
});
