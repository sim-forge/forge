import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter(),
    alias: {
      '$components': './src/app/components',
      '$stores': './src/app/stores',
      '$utils': './src/app/utils',
      '$styles': './src/app/styles'
    }
  }
};

export default config;