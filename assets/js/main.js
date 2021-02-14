/*
 * Main Javascript file for fm_frontend.
 *
 * This file bundles all of your javascript together using webpack.
 */

// JavaScript modules
require('@fortawesome/fontawesome-free');
const jQuery = require('jquery');
require('popper.js');
require('bootstrap');
require('malihu-custom-scrollbar-plugin');

require.context(
    '../img', // context folder
    true, // include subdirectories
    /.*/, // RegExp
  );

// Your own code
require('./plugins.js');
require('./script.js');
