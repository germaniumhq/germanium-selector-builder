const fs = require("fs");
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
  entry: ['./ts/main.ts'],
  output: {
    filename: 'js/main.js',
  },
  resolve: {
    extensions: ['', '.ts', '.tsx', '.js']
  },
  module: {
    loaders: [
      {
        test: function(name) {
          console.log(name);

          if (/\.tsx?$/.test(name)) {
            return true;
          }

          if (!/\./.test(name)) {
            return true;
          }

          return false;
        },
        exclude: /(node_modules|bower_components)/,
        loader: 'ts-loader',
      }
    ]
  },
  plugins: [
    new UglifyJSPlugin()
  ],
  devtool: 'source-map'
};

