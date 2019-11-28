const webpack = require("webpack");
const htmlWebpackPlugin = require("html-webpack-plugin");
const path = require("path");

module.exports = {
  outputDir: "../static",
  lintOnSave: process.env.NODE_ENV !== "production",
  productionSourceMap: false,
  devServer: {
    compress: true,
    port: 3000,
    hot: true,
    open: true,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  },
  configureWebpack: {
    // Set up all the aliases we use in our app.
    resolve: {
      alias: {
        "chart.js": "chart.js/dist/Chart.js"
      }
    },
    plugins: [
      new webpack.optimize.LimitChunkCountPlugin({
        maxChunks: 6
      }),
      new htmlWebpackPlugin({
        template: path.join(__dirname, "public/index.html"),
        inject: true,
        filename: path.join(__dirname, "../static/index.html")
      })
    ]
  },
  pwa: {
    name: "Guider Vue",
    themeColor: "#344675",
    msTileColor: "#344675",
    appleMobileWebAppCapable: "yes",
    appleMobileWebAppStatusBarStyle: "#344675"
  },
  css: {
    // Enable CSS source maps.
    sourceMap: process.env.NODE_ENV !== "production"
  }
};
