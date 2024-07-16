import path from 'path';

export default {
  base: "/static/",
  build: {
    //manifest: true,
    manifest: "manifest.json",
    outDir: path.resolve(__dirname, "dist"),
    rollupOptions: {
      input: {
        main: './src/js/main.js'
      }
    }
  },
  root: path.resolve(__dirname, 'src'),
  resolve: {
    alias: {
      '~bootstrap': path.resolve(__dirname, 'node_modules/bootstrap'),
      '~bootstrap-icons': path.resolve(__dirname, 'node_modules/bootstrap-icons'),
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    hot: true
  }
}
