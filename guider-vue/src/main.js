import 'babel-polyfill'
import Vue from 'vue'
import App from './App.vue'
import VueSocketIO from 'vue-socket.io'

Vue.config.productionTip = false
const serverAddr = process.env.NODE_ENV === 'development'
  ? 'http://localhost:5000' : document.getElementById('serverAddr').value

Vue.use(new VueSocketIO({
  debug: true,
  connection: serverAddr // 'http://localhost:5000'
}))

new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})
