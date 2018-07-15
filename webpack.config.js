const path = require('path');
const webpack = require('webpack');

/*
 * Webpack Plugins
 */
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

// take debug mode from the environment
const debug = (process.env.NODE_ENV !== 'production');

// Development asset host (webpack dev server)
const publicHost = debug ? 'http://192.168.2.105:2992' : '';

const rootAssetPath = path.join(__dirname, 'assets');

module.exports = {
  // configuration
  context: __dirname,
  entry: {
    app: './assets/js/index',
    main_js: './assets/js/main',
    main_css: [
      path.join(__dirname, 'node_modules', 'font-awesome', 'css', 'font-awesome.css'),
      path.join(__dirname, 'node_modules', 'bootstrap', 'dist', 'css', 'bootstrap.css'),
      path.join(__dirname, 'node_modules', 'malihu-custom-scrollbar-plugin', 'jquery.mCustomScrollbar.css'),
      path.join(__dirname, 'assets', 'css', 'style.css'),
      path.join(__dirname, 'assets', 'css', 'nav-style.css'),
    ],
  },
  output: {
    path: path.join(__dirname, 'fm_frontend', 'static', 'build'),
    publicPath: `${publicHost}/static/build/`,
    filename: '[name].[hash].js',
    chunkFilename: '[id].[hash].js',
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
        loader: ExtractTextPlugin.extract({ fallback: 'style-loader', use: 'css-loader!less-loader' }) 
      },
      { 
        test: /\.css$/,
        loader: ExtractTextPlugin.extract({ fallback: 'style-loader', use: 'css-loader' }) 
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
    new ExtractTextPlugin('[name].[hash].css'),
    new webpack.ProvidePlugin({ $: 'jquery', jQuery: 'jquery' }),
    new ManifestRevisionPlugin(path.join(__dirname, 'fm_frontend', 'webpack', 'manifest.json'), {
      rootAssetPath: rootAssetPath,
      // explicity include img/* assets
      extensionsRegex: /(\/img\/)/i,
      ignorePaths: ['/js', '/css'],
    }),
    new VueLoaderPlugin()
  ].concat(debug ? [] : [
    // production webpack plugins go here
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production'),
      }
    }),
  ]),
};
