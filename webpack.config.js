const path = require('path');
const webpack = require('webpack');

/*
 * Webpack Plugins
 */
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

const ProductionPlugins = [
  // production webpack plugins go here
  new webpack.DefinePlugin({
    "process.env": {
      NODE_ENV: JSON.stringify("production")
    }
  })
]

// take debug mode from the environment
const debug = (process.env.NODE_ENV !== 'production');
const rootAssetPath = path.join(__dirname, 'assets');
const env_mode = process.env.NODE_ENV

module.exports = {
  // configuration
  context: __dirname,
  entry: {
    app: './assets/js/index',
    main_js: './assets/js/main',
    main_css: [
      path.join(__dirname, 'assets', 'css', 'style.css'),
      path.join(__dirname, 'assets', 'css', 'nav-style.css'),
    ],
    vendor_css: [
      path.join(__dirname, 'node_modules', '@fortawesome', 'fontawesome-free', 'css', 'all.css'),
      path.join(__dirname, 'node_modules', 'bootstrap', 'dist', 'css', 'bootstrap.css'),
      path.join(__dirname, 'node_modules', 'malihu-custom-scrollbar-plugin', 'jquery.mCustomScrollbar.css'),
    ]
  },
  mode: env_mode,
  watch: debug,
  // could not get watch working without adding poll. Probably due to using docker with Windows and WSL2
  watchOptions: {
    aggregateTimeout: 200,
    poll: 1000,
    ignored: ['/node_modules/', '__pycache__']
  },
  output: {
    chunkFilename: "[id].js",
    filename: "[name].bundle.js",
    path: path.join(__dirname, "fm_frontend", "static", "build"),
    publicPath: "/static/build/",
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css', '.vue'],
    alias:{
      'vue$': 'vue/dist/vue.esm.js'
    },
  },
  devtool: debug ? "eval-source-map" : false,
  plugins: [
    new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
    new webpack.ProvidePlugin({ $: 'jquery', jQuery: 'jquery' }),
    new VueLoaderPlugin(),
  ].concat(debug ? [] : ProductionPlugins),
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      { 
        test: /\.less$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          'css-loader!less-loader' 
        ],
      },
      { 
        test: /\.html$/,
        loader: 'raw-loader' 
      },
      {
        test: /\.css$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          'css-loader',
        ],
      },
      { 
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: 'url-loader', options: {limit: 10000, mimetype: 'application/font-woff' }
      },
      { 
        test: /\.(ttf|eot|svg|png|jpe?g|gif|ico)(\?.*)?$/i,
        loader: 'file-loader',
        options: {
          context: rootAssetPath,
          name: '[path][name].[ext]'
        }
      },
      { 
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        options: { 
          presets: ["@babel/preset-env"],
          cacheDirectory: true
        } 
      },
      {
        // see https://github.com/webpack/webpack/issues/11467
        test: /\.m?js$/,
        resolve: {
          fullySpecified: false
        }
      },
    ],
  },
};
