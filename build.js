const esbuild = require('esbuild');
const vuePlugin = require('esbuild-plugin-vue');

esbuild.build({
  entryPoints: ['./src/main.js'], // 你的入口文件
  bundle: true,
  outfile: './dist/bundle.js', // 打包輸出的文件
  plugins: [vuePlugin()], // 添加 Vue 插件
  loader: { '.js': 'jsx' }, // 如果有用到 JSX，可以加上這行
  define: { 'process.env.NODE_ENV': '"production"' }, // 確保 Vue 以生產模式運行
}).catch(() => process.exit(1));
