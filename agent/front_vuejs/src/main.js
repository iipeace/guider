import Vue from 'vue'
import App from './App.vue'
//import socketio from 'socket.io'
import VueSocketIO from 'vue-socket.io'
//import SocketIO from './SocketIO.vue'

Vue.config.productionTip = false;

Vue.use(new VueSocketIO({
    debug: true,
    connection: 'http://127.0.0.1:5000' //'http://localhost:5000'
}))

new Vue({
  el: '#app',
  components: { App },
  template: "<App/>"
  //render: h => h(App)
});
