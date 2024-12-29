const esbuild = require('esbuild');
const vue = require('esbuild-plugin-vue3');

// 檢查是否有 --watch 參數
const isWatch = process.argv.includes('--watch');

// 建立基本配置
const buildOptions = {
  entryPoints: ['./frontend/scripts/app.js'],
  bundle: true,
  outfile: './static/scripts/app.js',
  plugins: [vue()],
  loader: { '.js': 'jsx' },
  define: { 'process.env.NODE_ENV': '"production"' }
};

// 根據是否為 watch 模式選擇不同的建構方法
if (isWatch) {
  // watch 模式
  esbuild
    .context(buildOptions)
    .then(context => {
      // 開始 watch
      context.watch();
      console.log('Watching for changes...');
    })
    .catch(() => process.exit(1));
} else {
  // 一般建構模式
  esbuild
    .build(buildOptions)
    .then(() => console.log('Build complete'))
    .catch(() => process.exit(1));
}