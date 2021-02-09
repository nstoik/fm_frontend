const path = require('path');
const webpack = require('webpack');

/*
 * Webpack Plugins
 */
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const ManifestPlugin = require('webpack-manifest-plugin');
const IgnoreEmitPlugin = require('ignore-emit-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

// take debug mode from the environment
const debug = (process.env.NODE_ENV !== 'production');
const hashType = debug ? '[hash]': '[contentHash]'

// Development asset host (webpack dev server)
console.log('debug value is: ' + debug)
const publicHost = debug ? 'http://127.0.0.1:2992' : '';

const rootAssetPath = path.join(__dirname, 'assets');

module.exports = {
  // configuration
  context: __dirname,
  entry: {
    app: './assets/js/index',
    main_js: './assets/js/main',
    main_css: [
      path.join(__dirname, 'node_modules', '@fortawesome', 'fontawesome-free', 'css', 'fontawesome.css'),
      path.join(__dirname, 'node_modules', 'bootstrap', 'dist', 'css', 'bootstrap.css'),
      path.join(__dirname, 'node_modules', 'malihu-custom-scrollbar-plugin', 'jquery.mCustomScrollbar.css'),
      path.join(__dirname, 'assets', 'css', 'style.css'),
      path.join(__dirname, 'assets', 'css', 'nav-style.css'),
    ],
  },
  output: {
    path: path.join(__dirname, 'fm_frontend', 'static'),
    publicPath: `${publicHost}/static/`,
    filename: "js/[name]." + hashType + ".js",
    chunkFilename: "js/[name]." + hashType + ".chunk.js"
  },
  optimization: {
    minimizer: [
      new TerserPlugin({
          test: /\.js(\?.*)?$/i,
          sourceMap: true,
      }),
      new OptimizeCssAssetsPlugin({
        assetNameRegExp: /\.css$/g,
        cssProcessor: require('cssnano'),
        cssProcessorPluginOptions: {
          preset: ['default', { discardComments: { removeAll: true } }],
        },
        canPrint: true
      }),
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css', '.vue'],
    alias:{
      img: path.join(__dirname, 'assets', 'img'),
      'vue$': 'vue/dist/vue.esm.js'
    },
  },
  devtool: 'source-map',
  devServer: {
    headers: { 'Access-Control-Allow-Origin': '*' },
    publicPath: `${publicHost}/static/`,
    public: `${publicHost}`
  },
  module: {
    rules: [
      { 
        test: /\.html$/,
        loader: 'raw-loader' 
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      { 
        test: /\.less$/,
        use: [MiniCssExtractPlugin.loader,'css-loader!less-loader' ] ,
      },
      {
        test: /\.css$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              hmr: debug,
            },
          },
          'css-loader',
          {
            loader: 'postcss-loader'
          }
        ],
      },
      { 
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: 'url-loader?limit=10000&mimetype=application/font-woff'
      },
      { 
        test: /\.(ttf|eot|svg|png|jpe?g|gif|ico)(\?.*)?$/i,
        loader: `file-loader?context=${rootAssetPath}&name=[path][name].[hash].[ext]`
      },
      { 
        test: /\.js$/,
        exclude: file => (
          /node_modules/.test(file) &&
          !/\.vue\.js/.test(file)
        ),
        loader: 'babel-loader',
        options: { 
          presets: ['env'],
          plugins: ['transform-object-rest-spread'],
          cacheDirectory: true
        } 
      },
    ],
  },
  plugins: [
    new IgnoreEmitPlugin(/(?<=main_css\s*).*?(?=\s*js)/gs),
    new MiniCssExtractPlugin({ filename: 'css/[name].' + hashType + '.css', }),
    new webpack.ProvidePlugin({ $: 'jquery', jQuery: 'jquery' }),
    new VueLoaderPlugin(),
    new ManifestPlugin(
      {
          map: (file) => {
          // Remove hash in manifest key
          file.name = file.name.replace(/(\.[a-f0-9]{32})(\..*)$/, '$2');
          return file;
          },
          writeToFileEmit: true,
      }),
  ].concat(debug ? [] : [
    // production webpack plugins go here
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production'),
      }
    }),
    new CleanWebpackPlugin(),
  ]),
};
